from django.views import View
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.http import JsonResponse, HttpResponse
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.core.cache import cache
# ---------------------------------------------
import json
import pandas as pd
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db import IntegrityError
from django.db.models import Case, When, Value
from django.db.models import CharField
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.template.loader import get_template
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
##############################################
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
############################################
from corepy.forms import LoginFormWithCaptcha
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.core.cache import cache
from django.contrib.sessions.models import Session

from corepy.models import Site, Readings, SiteInfo, ExceedanceReports
from django.contrib.auth.models import User


def update_site_status(func):
    def wrapper(*args, **kwargs):
        # Define time thresholds
        current_time = timezone.now()
        six_hours_ago = current_time - timedelta(hours=6)
        twenty_four_hours_ago = current_time - timedelta(hours=24)

        # Calculate new status for each SiteInfo entry and update Site model
        site_info_queryset = SiteInfo.objects.select_related('site').annotate(
            new_status=Case(
                When(timestamp__gt=six_hours_ago, then=Value('Live')),
                When(timestamp__gt=twenty_four_hours_ago, then=Value('Delay')),
                default=Value('Offline'),
                output_field=CharField()
            )
        )
        # Bulk update all sites with their corresponding statuses
        site_bulk_update_list = []
        for site_info in site_info_queryset:
            site = site_info.site
            if site.status != site_info.new_status:
                site.status = site_info.new_status
                site_bulk_update_list.append(site)

        # Perform bulk update
        if site_bulk_update_list:
            Site.objects.bulk_update(site_bulk_update_list, ['status'])

        # Proceed to the original function
        return func(*args, **kwargs)

    return wrapper


class ProtectedView(View):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProtectedView, self).dispatch(request, *args, **kwargs)



def logoutapp(request):
    logout(request)
    request.session.flush()
    captcha_key = CaptchaStore.generate_key()
    captcha_image = captcha_image_url(captcha_key)
    form = LoginFormWithCaptcha()
    context = {
        'form': form,
        'captcha_key': captcha_key,
        'captcha_image': captcha_image,
        'next': request.GET.get('next', '')
    }
    response = render(request, 'login.html', context)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


def logout_other_sessions(user, current_session_key=None):
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    for session in sessions:
        data = session.get_decoded()
        if data.get('_auth_user_id') == str(user.id):
            if current_session_key and session.session_key == current_session_key:
                continue
            session.delete()



@csrf_protect
def signin(request):
    if request.user.is_authenticated:
        login(request, user)
        return redirect('corepy:dashboard')
    captcha_key = CaptchaStore.generate_key()
    captcha_image = captcha_image_url(captcha_key)
    if request.method == "POST":
        print(request.POST)
        identifier = request.POST.get('email')
        password = request.POST.get('password')
        captcha_0 = request.POST.get('captcha_0')
        captcha_1 = request.POST.get('captcha_1')
        attempts = cache.get(f'login_attempts_{identifier}', 0)
        if attempts >= 3:
            messages.error(
                request,
                "Too many login attempts. Please try again after 5 minutes."
            )
            return render(request, "login.html", {
                "captcha_key": captcha_key,
                "captcha_image": captcha_image
            })
        try:
            captcha = CaptchaStore.objects.get(hashkey=captcha_0)

            if captcha.response.lower() != captcha_1.lower():
                messages.error(request, "CAPTCHA is incorrect.")
                cache.set(
                    f'login_attempts_{identifier}',
                    attempts + 1,
                    timeout=300
                )
            else:
                user_obj = User.objects.filter(email=identifier).first()
                if user_obj:
                    user = authenticate(
                        request,
                        username=user_obj.username,
                        password=password)
                else:
                    user = authenticate(
                        request,
                        username=identifier,
                        password=password)
                if user and user.is_active:
                    login(request, user)
                    request.session.cycle_key()
                    request.session.set_expiry(1800)
                    logout_other_sessions(
                        user,
                        current_session_key=request.session.session_key)
                    cache.delete(f'login_attempts_{identifier}')
                    return redirect('corepy:dashboard')
                else:
                    messages.error(
                        request,
                        "Invalid email or password.")
                    cache.set(
                        f'login_attempts_{identifier}',
                        attempts + 1,
                        timeout=300)
        except CaptchaStore.DoesNotExist:
            messages.error(
                request,
                "CAPTCHA validation failed.")
            cache.set(
                f'login_attempts_{identifier}',
                attempts + 1,
                timeout=300)
        captcha_key = CaptchaStore.generate_key()
        captcha_image = captcha_image_url(captcha_key)
    return render(request, 'login.html', {
        'captcha_key': captcha_key,
        'captcha_image': captcha_image })


class WelcomeView(ProtectedView):
    @update_site_status
    def get(self, request):
        tmplt = get_template("pages/dashboard.html")
        context = {
            # "sites": sites,
            # "live_sites": sites.filter(status="Live").count(),
            # "delay_sites": sites.filter(status="Delay").count(),
            # "offline_sites": sites.filter(status="Offline").count(),
        }
        html = tmplt.render(context, request)
        return HttpResponse(html)


class PublicDashboardView(View):
    @update_site_status
    def get(self, request):
        tmplt = get_template("pages/public_dashboard.html")
        # all_sites = Site.objects.all()
        sites = Site.objects.exclude(industry__name="Kamarajar Port Limited Chennai")  # Exclude specific industry
        context = {
            "sites": sites,
            "live_sites": sites.filter(status="Live").count(),
            "delay_sites": sites.filter(status="Delay").count(),
            "offline_sites": sites.filter(status="Offline").count(),
        }
        html = tmplt.render(context, request)
        return HttpResponse(html)


class UploadView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        ts_format = "%Y-%m-%d %H:%M:%S"
        site_readings = []

        try:
            data = request.data['payload']
            site = data['site']
            readings = data['data']

            for record in readings:
                tmp = {}
                _reading = {}
                reading = record['reading']

                for k, val in reading.items():
                    try:
                        val = float(val)
                        val = round(val, 3)
                        _reading[k.lower()] = val
                    except ValueError:
                        pass

                if _reading:
                    # Handle site not found error
                    try:
                        tmp['site'] = Site.objects.get(prefix__iexact=site['prefix'])
                    except Site.DoesNotExist:
                        return Response(
                            {'msg': f"Site with prefix '{site['prefix']}' does not exist"},
                            status=status.HTTP_404_NOT_FOUND)

                    tmp['reading'] = _reading
                    tmp['timestamp'] = datetime.strptime(record['timestamp'], ts_format)
                    site_readings.append(tmp)

            if site_readings:
                try:
                    Readings.objects.bulk_create(
                        [Readings(**q) for q in site_readings],
                        batch_size=100,
                        ignore_conflicts=True
                    )

                    # Get the most recent reading
                    latest_reading = max(site_readings, key=lambda x: x['timestamp'])
                    site_instance = latest_reading['site']
                    reading_data = latest_reading['reading']
                    timestamp_data = latest_reading['timestamp']
                    # Update or create SiteInfo
                    SiteInfo.objects.update_or_create(
                        site=site_instance,
                        defaults={
                            # 'last_seen': timezone.now(),  # Store current time as last seen
                            'reading': reading_data,  # Update reading field
                            'timestamp': timestamp_data  # Update timestamp field
                        }
                    )

                    return Response({'msg': 'success'}, status=status.HTTP_201_CREATED)
                except IntegrityError:
                    return Response({'msg': 'record(s) of this exists'},
                                    status=status.HTTP_208_ALREADY_REPORTED)
            else:
                return Response({'msg': 'no records in payload'},
                                status=status.HTTP_400_BAD_REQUEST)

        except KeyError:
            return Response({'msg': 'incorrect payload'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as err:
            return Response({'msg': f'{err.__str__()}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SiteView(ProtectedView):
    def get(self, request, id=None, **kwargs):
        info_template = get_template('pages/site-detail.html')
        site = Site.objects.get(id=id)
        markers = []
        markers.append({
            "latitude": float(site.latitude),
            "longitude": float(site.longitude),
            "location": site.address.replace("\r", "\\r").replace("\n", "\\n"),
        })
        now = datetime.now()
        # start_of_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        start_of_today = now - timedelta(days=7)
        records = Readings.objects.filter(site=site, timestamp__gte=start_of_today)
        record_data = [{'timestamp': record.timestamp, **record.reading} for record in records]
        record_df = pd.DataFrame(record_data)
        if not record_df.empty:
            record_df['timestamp'] = record_df['timestamp'] + timedelta(hours=5, minutes=30)
        record_df = record_df.fillna('')
        record_dict = record_df.to_dict(orient="records")

        for rec in record_dict:
            rec['timestamp'] = rec['timestamp'].strftime('%Y-%m-%d %H:%M:%S')

        context = {"site": site, "map_markers": json.dumps(markers),
                   "record_dict": record_dict, 'reading': record_dict[-1] if record_data else []}
        html = info_template.render(context, request)
        return HttpResponse(html)


class NewSiteView(View):

    def get(self, request, id=None, **kwargs):
        info_template = get_template('pages/new-site-details.html')
        site = Site.objects.get(id=id)
        markers = []
        markers.append({
            "latitude": float(site.latitude),
            "longitude": float(site.longitude),
            "location": site.address.replace("\r", "\\r").replace("\n", "\\n"),
        })

        now = datetime.now()
        # start_of_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        start_of_today = now - timedelta(days=7)

        records = Readings.objects.filter(site=site, timestamp__gte=start_of_today)
        record_data = [{'timestamp': record.timestamp, **record.reading} for record in records]
        record_df = pd.DataFrame(record_data)
        if not record_df.empty:
            record_df['timestamp'] = record_df['timestamp'] + timedelta(hours=5, minutes=30)
        record_df = record_df.fillna('')
        record_dict = record_df.to_dict(orient="records")

        for rec in record_dict:
            rec['timestamp'] = rec['timestamp'].strftime('%Y-%m-%d %H:%M:%S')

        context = {"site": site, "map_markers": json.dumps(markers),
                   "record_dict": record_dict, 'reading': record_dict[-1] if record_data else []}
        html = info_template.render(context, request)
        return HttpResponse(html)


def site_chart_detail(request, id):
    siteObj = Site.objects.get(id=id)
    date_range = request.GET.get("daterange")
    date_parts = date_range.split("-")

    if len(date_parts) != 2:
        return JsonResponse({"error": "Invalid date range format"}, status=400)

    try:
        start_date = datetime.strptime(date_parts[0].strip(), "%d/%m/%Y")
        end_date = datetime.strptime(date_parts[1].strip(), "%d/%m/%Y")
    except ValueError:
        return JsonResponse({"error": "Invalid date format"}, status=400)

    end_date += timedelta(days=1)

    records = Readings.objects.filter(site=siteObj, timestamp__gte=start_date,
                                      timestamp__lte=end_date)
    print(records,"recordsrecordsrecordsrecordsrecordsrecordsrecordsrecordsrecordsrecords")
    record_data = [{'timestamp': record.timestamp, **record.reading} for record in records]
    record_df = pd.DataFrame(record_data)

    if not record_df.empty:
        record_df['timestamp'] = pd.to_datetime(record_df['timestamp'])
        record_df['timestamp'] = record_df['timestamp'] + timedelta(hours=5, minutes=30)

        record_df.fillna(0, inplace=True)

        # Sort DataFrame by 'timestamp' in ascending order
        record_df.sort_values('timestamp', inplace=True)

        # Optional: Resetting index after sorting
        record_df.reset_index(drop=True, inplace=True)
    record_dict = record_df.to_dict(orient="records")

    for rec in record_dict:
        rec['timestamp'] = rec['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
    return JsonResponse({"record_dict": record_dict})


# def reports(request):
#     info_template = get_template('reports/report.html')
#     siteObj = Site.objects.all()
#     html = info_template.render({"siteObj": siteObj}, request)
#     return HttpResponse(html)

def reports(request):
    info_template = get_template('reports/report.html')
    siteObj = Site.objects.all()
    if request.user.is_authenticated and request.user.email == "customer@tpro.com":
        allowed_prefixes = ["cargoberth1", "fingerjetty3"]
        siteObj = siteObj.filter(prefix__in=allowed_prefixes)
    html = info_template.render({"siteObj": siteObj}, request)
    return HttpResponse(html)

def new_reports(request):
    info_template = get_template('reports/new_report.html')
    siteObj = Site.objects.all()
    print(siteObj,"------------------")
    html = info_template.render({"siteObj": siteObj}, request)
    return HttpResponse(html)


def fetch_site_data_report(request):
    site_uuid = request.GET.get("site-uuid")
    date_range = request.GET.get("daterange")
    date_parts = date_range.split("-")

    if len(date_parts) != 2:
        return JsonResponse({"error": "Invalid date range format"}, status=400)

    try:
        start_date = datetime.strptime(date_parts[0].strip(), "%m/%d/%Y")
        end_date = datetime.strptime(date_parts[1].strip(), "%m/%d/%Y")
    except ValueError:
        return JsonResponse({"error": "Invalid date format"}, status=400)

    try:
        siteObj = Site.objects.get(id=site_uuid)
        site_name = siteObj.name
    except Site.DoesNotExist:
        return JsonResponse({"error": "Site not found"}, status=404)

    end_date += timedelta(
        days=1)  # Incrementing end date by one day to include records on the end date
    readingObj = Readings.objects.filter(site=siteObj, timestamp__range=[start_date, end_date])
    data = serializers.serialize('python', readingObj, fields=('timestamp', 'reading'))
    records = []
    for entry in data:
        fields = entry['fields']
        timestamp = fields['timestamp']
        reading = fields['reading']
        if reading:
            records.append([timestamp, reading])

    df = pd.DataFrame(records, columns=['timestamp', 'reading'])
    # df['reading'] = df['reading'].apply(json.loads)
    df_normalized = pd.json_normalize(df['reading'])
    df = pd.concat([df, df_normalized], axis=1)
    df = df.drop('reading', axis=1)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    if not df.empty:
        df['timestamp'] = df['timestamp'] + timedelta(hours=5, minutes=30)
        df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
    df = df.set_index('timestamp')
    df = df.reset_index()
    df = df.astype(str)

    # df = pd.DataFrame.from_records(readingObj)
    # if not df.empty:
    #     df['timestamp'] = df['timestamp'] + timedelta(hours=5, minutes=30)
    #     # df.drop_duplicates("timestamp")
    #     # df = df.sort_values(by='timestamp')

    json_data = df.to_dict(orient='records')

    return JsonResponse({"data": json_data, "site_name": site_name})


def exc_reports(request):
    info_template = get_template('reports/exc_reports.html')
    siteObj = Site.objects.all()
    html = info_template.render({"siteObj": siteObj}, request)
    return HttpResponse(html)


def site_exceedance_report(request):
    try:
        site_uuid = request.GET.get("site-uuid")
        date_range_str = request.GET.get("daterange")

        if not site_uuid or not date_range_str:
            return JsonResponse({"error": "Missing site UUID or date range"}, status=400)

        date_range_parts = date_range_str.split("-")
        if len(date_range_parts) != 2:
            return JsonResponse({"error": "Invalid date range format"}, status=400)

        try:
            # Parse start and end date, and make timezone aware
            start_date = datetime.strptime(date_range_parts[0].strip(), "%m/%d/%Y")
            end_date = datetime.strptime(date_range_parts[1].strip(), "%m/%d/%Y") + timedelta(
                days=1)

            start_date = timezone.make_aware(start_date)
            end_date = timezone.make_aware(end_date)
        except ValueError:
            return JsonResponse({"error": "Invalid date format"}, status=400)

        try:
            site = Site.objects.get(id=site_uuid)
            site_name = site.name
        except Site.DoesNotExist:
            return JsonResponse({"error": "Site not found"}, status=404)

        # Filter using aware datetimes
        reports = ExceedanceReports.objects.filter(
            site=site,
            timestamp__range=[start_date, end_date]
        )
        data = serializers.serialize('python', reports, fields=(
            'timestamp', 'parameter', 'value', 'min', 'max', 'comment'))
        records_list = []
        for entry in data:
            fields = entry['fields']
            try:
                records_list.append({
                    "timestamp": fields['timestamp'],
                    "parameter": fields['parameter'],
                    "value": float(fields['value']),
                    "min": float(fields['min']),
                    "max": float(fields['max']),
                    "comment": fields.get('comment', '')
                })
            except KeyError as e:
                print("Missing field:", e)
                continue

        df = pd.DataFrame(records_list)
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')

        return JsonResponse({"data": df.to_dict(orient='records'), "site_name": site_name})

    except Exception as e:
        return JsonResponse({"error": "Internal server error"}, status=500)
