// // $(document).ready(function () {
// //   getDevices();
// // });
// let markers = [];

// function getDevices() {
//   var deviceURL =
//     "/site_data";
//   $.ajax({
//     type: "GET",
//     url: "/site_data",
//     contentType: "text/plain",
//     dataType: "json",
//     success: function (data) {
//       console.log("data :- ", data);
//       populateDataTable(deviceData);
//     },
//     error: function (e) {
//       console.log("There was an error with your request...");
//       console.log("error: " + JSON.stringify(e));
//     },
//   });
// }

// function populateDataTable(data) {
//   let columns = [];
//   $.each(data[0], function (name, value) {
//     if (name != "uid") {
//       var column = {
//         data: name,
//         title: name,
//       };
//       columns.push(column);
//     }
//   });
//   $.each(data, function (name, value) {
//     markers.push({
//       latitude: value.Latitude,
//       longitude: value.Longitude,
//       location: value.location,
//     });
//   });
//   initMap(markers);

//   $("#table_devices").DataTable({
//     columns: [
//       {
//         title: "Device ID",
//         data: "DWLR SR NO",
//       },
//       { title: "Location", data: "location" },
//       {
//         title: "Date & Time",
//         data: null,
//         render: function (data, type, row) {
//           return "";
//         },
//       },
//       {
//         title: "Battery",
//         data: null,
//         render: function (data, type, row) {
//           return "";
//         },
//       },
//       {
//         title: "Water Level",
//         data: null,
//         render: function (data, type, row) {
//           return "";
//         },
//       },
//       {
//         title: "Water Temp",
//         data: null,
//         render: function (data, type, row) {
//           return "";
//         },
//       },
//       {
//         title: "Active",
//         data: "Status",
//         render: function (data, type, row) {
//           return data?.toLowerCase() === "completed" ? 
//             '<i class="fa-solid fa-thumbs-up" style="color: #4e9a06;"></i>'
//               : 
//             '<i class="fa-regular fa-thumbs-down" style="color: #a40000;"></i>'
//         },
//       },
//     ],
//     data: data,
//     aLengthMenu: [
//       [20, 50, 100, -1],
//       [20, 50, 100, "All"],
//     ],
//     "columnDefs": [
//       { "targets": [-1], "orderable": false }
//   ],
//     fnRowCallback: function (nRow, aData, iDisplayIndex) {
//       // Bind click event
//       $(nRow).click(function () {
//         let sensorId = aData["DWLR SR NO"];
//         document.location.href = "/device/=" + sensorId;
//       });
//       return nRow;
//     },
//   });
// }

// function initMap(locations) {
//   var map = new google.maps.Map(document.getElementById("map"), {
//     zoom: 11,
//     center: new google.maps.LatLng(28.7332, 77.1974),
//     mapTypeId: google.maps.MapTypeId.ROADMAP,
//     styles: [
//       {
//         featureType: "administrative",
//         elementType: "labels.text.fill",
//         stylers: [
//           {
//             color: "#444444",
//           },
//         ],
//       },
//       {
//         featureType: "landscape",
//         elementType: "all",
//         stylers: [
//           {
//             color: "#f2f2f2",
//           },
//         ],
//       },
//       {
//         featureType: "poi",
//         elementType: "all",
//         stylers: [
//           {
//             visibility: "off",
//           },
//         ],
//       },
//       {
//         featureType: "road",
//         elementType: "all",
//         stylers: [
//           {
//             saturation: -100,
//           },
//           {
//             lightness: 45,
//           },
//         ],
//       },
//       {
//         featureType: "road.highway",
//         elementType: "all",
//         stylers: [
//           {
//             visibility: "simplified",
//           },
//         ],
//       },
//       {
//         featureType: "road.arterial",
//         elementType: "labels.icon",
//         stylers: [
//           {
//             visibility: "off",
//           },
//         ],
//       },
//       {
//         featureType: "transit",
//         elementType: "all",
//         stylers: [
//           {
//             visibility: "off",
//           },
//         ],
//       },
//       {
//         featureType: "water",
//         elementType: "all",
//         stylers: [
//           {
//             color: "#00b7ff",
//           },
//           {
//             visibility: "on",
//           },
//         ],
//       },
//     ],
//   });

//   var infowindow = new google.maps.InfoWindow();
//   var marker, i;

//   for (i = 0; i < locations.length; i++) {
//     marker = new google.maps.Marker({
//       position: new google.maps.LatLng(
//         locations[i]["latitude"],
//         locations[i]["longitude"]
//       ),
//       map: map,
//     });
//     google.maps.event.addListener(
//       marker,
//       "click",
//       (function (marker, i) {
//         return function () {
//           infowindow.setContent(locations[i]["location"]);
//           infowindow.open(map, marker);
//         };
//       })(marker, i)
//     );
//   }
// }

// const deviceData = [
//   {
//     "Zone wise Numbering": 1,
//     "  State  ": "Delhi",
//     "District ": "Central",
//     Block: "CIVIL LINE5",
//     location: "Burari OJB Ex. Eng Office",
//     Latitude: 28.7332,
//     Longitude: 77.1974,
//     "Depth constructed (m)": 46.0,
//     "Tentative depth of installation of DWLR (m)": 15,
//     "Depth from ground measurement": "e",
//     "DWLR SR NO": "AAXI127",
//     Status: "Completed ",
//   },
//   {
//     "Zone wise Numbering": 2,
//     "  State  ": "Delhi",
//     "District ": "Nazul Land",
//     Block: "NAZUL LAND",
//     location: "Lalita Park (Pz)",
//     Latitude: 28.6325,
//     Longitude: 77.2717,
//     "Depth constructed (m)": 82.0,
//     "Tentative depth of installation of DWLR (m)": 15,
//     "Depth from ground measurement": "e",
//     "DWLR SR NO": "AAXI089",
//     Status: "Completed ",
//   },
//   {
//     "Zone wise Numbering": 3,
//     "  State  ": "Delhi",
//     "District ": "New Delhi",
//     Block: "CHANAKYAPUR I",
//     location: "LodhiGarden (Deep)",
//     Latitude: 28.5903,
//     Longitude: 77.2164,
//     "Depth constructed (m)": 63.0,
//     "Tentative depth of installation of DWLR (m)": 20,
//     "Depth from ground measurement": "e",
//     "DWLR SR NO": "AAXI010",
//     Status: "Completed ",
//   },
//   {
//     "Zone wise Numbering": 4,
//     "  State  ": "Delhi",
//     "District ": "New Delhi",
//     Block: "CHANAKYAPUR I",
//     location: "LodhiGarden(5hallow)",
//     Latitude: 28.5903,
//     Longitude: 77.2164,
//     "Depth constructed (m)": 60.0,
//     "Tentative depth of installation of DWLR (m)": 20,
//     "Depth from ground measurement": "e",
//     "DWLR SR NO": "AAXI039",
//     Status: "Completed ",
//   },
//   {
//     "Zone wise Numbering": 5,
//     "  State  ": "Delhi",
//     "District ": "New Delhi",
//     Block: "CHANAKYAPUR I",
//     location: "Sunder Nursery Pz",
//     Latitude: 28.5961,
//     Longitude: 77.245,
//     "Depth constructed (m)": 62.0,
//     "Tentative depth of installation of DWLR (m)": 18,
//     "Depth from ground measurement": "e",
//     "DWLR SR NO": "AAXI003",
//     Status: "Completed ",
//   },
//   {
//     "Zone wise Numbering": 6,
//     "  State  ": "Delhi",
//     "District ": "New Delhi",
//     Block: "DELHICANTONMENT",
//     location: "Kabulline Pz",
//     Latitude: 28.5922,
//     Longitude: 77.1275,
//     "Depth constructed (m)": 48.0,
//     "Tentative depth of installation of DWLR (m)": 45,
//     "Depth from ground measurement": "e",
//     "DWLR SR NO": "AAXI007",
//     Status: "completed",
//   },
//   {
//     "Zone wise Numbering": 7,
//     "  State  ": "Delhi",
//     "District ": "North",
//     Block: "ALIPUR",
//     location: "Bakoli Deep Pz",
//     Latitude: 28.8153,
//     Longitude: 77.1517,
//     "Depth constructed (m)": 40.0,
//     "Tentative depth of installation of DWLR (m)": 22,
//     "Depth from ground measurement": 10.1,
//     "DWLR SR NO": "AAXI141",
//     Status: "completed",
//   },
//   {
//     "Zone wise Numbering": 8,
//     "  State  ": "Delhi",
//     "District ": "North",
//     Block: "ALIPUR",
//     location: "Bakolishallow",
//     Latitude: 28.8153,
//     Longitude: 77.1517,
//     "Depth constructed (m)": 35.0,
//     "Tentative depth of installation of DWLR (m)": 20,
//     "Depth from ground measurement": 9.79,
//     "DWLR SR NO": "AAXI122",
//     Status: "completed",
//   },
//   {
//     "Zone wise Numbering": 9,
//     "  State  ": "Delhi",
//     "District ": "North",
//     Block: "Model Town",
//     location: "Coronation Pillar",
//     Latitude: 28.7245,
//     Longitude: 77.1925,
//     "Depth constructed (m)": 56.0,
//     "Tentative depth of installation of DWLR (m)": 15,
//     "Depth from ground measurement": "e",
//     "DWLR SR NO": "AAXI111",
//     Status: "Completed ",
//   },
//   {
//     "Zone wise Numbering": 10,
//     "  State  ": "Delhi",
//     "District ": "North",
//     Block: "Model Town",
//     location: "Kewal Park",
//     Latitude: 28.7185,
//     Longitude: 77.1812,
//     "Depth constructed (m)": 77.0,
//     "Tentative depth of installation of DWLR (m)": 15,
//     "Depth from ground measurement": "e",
//     "DWLR SR NO": "AAXI058",
//     Status: "Completed ",
//   },
//   {
//     "Zone wise Numbering": 11,
//     "  State  ": "Delhi",
//     "District ": "North East",
//     Block: "Karawal Nagar",
//     location: "Sonia Vihar",
//     Latitude: 28.7078,
//     Longitude: 77.249,
//     "Depth constructed (m)": 44.0,
//     "Tentative depth of installation of DWLR (m)": 20,
//     "Depth from ground measurement": "e",
//     "DWLR SR NO": "AAXI116",
//     Status: "Completed ",
//   },
//   {
//     "Zone wise Numbering": 12,
//     "  State  ": "Delhi",
//     "District ": "North West",
//     Block: "ROHINI",
//     location: "Rohini Sector 1Pz",
//     Latitude: 28.7028,
//     Longitude: 77.0981,
//     "Depth constructed (m)": 47.0,
//     "Tentative depth of installation of DWLR (m)": 15,
//     "Depth from ground measurement": 2.5,
//     "DWLR SR NO": "AAXI123",
//     Status: "Completed ",
//   },
//   {
//     "Zone wise Numbering": 13,
//     "  State  ": "Delhi",
//     "District ": "North West",
//     Block: "SARASWATIVIHAR",
//     location: "Sandesh Vihar Pz",
//     Latitude: 28.695,
//     Longitude: 77.1461,
//     "Depth constructed (m)": 42.0,
//     "Tentative depth of installation of DWLR (m)": 15,
//     "Depth from ground measurement": "5.3 m",
//     "DWLR SR NO": "AAXI066",
//     Status: "completed",
//   },
//   {
//     "Zone wise Numbering": 14,
//     "  State  ": "Delhi",
//     "District ": "North West",
//     Block: "SARASWATIVIHAR",
//     location: "Sanjay Van Pz",
//     Latitude: 28.6903,
//     Longitude: 77.1419,
//     "Depth constructed (m)": 37.0,
//     "Tentative depth of installation of DWLR (m)": 15,
//     "Depth from ground measurement": "3.3 m",
//     "DWLR SR NO": "AAXI142",
//     Status: "Completed ",
//   },
//   {
//     "Zone wise Numbering": 15,
//     "  State  ": "Delhi",
//     "District ": "South East",
//     Block: "SARITA VIHAR",
//     location: "Jaitpur Khadar RD3500 Pz",
//     Latitude: 28.5089,
//     Longitude: 77.3406,
//     "Depth constructed (m)": 33.0,
//     "Tentative depth of installation of DWLR (m)": 20,
//     "Depth from ground measurement": "e",
//     "DWLR SR NO": "AAXI008",
//     Status: "Completed ",
//   },
//   {
//     "Zone wise Numbering": 16,
//     "  State  ": "Delhi",
//     "District ": "South West",
//     Block: "NAJAFGARH",
//     location: "Ujwah Pz",
//     Latitude: 28.5767,
//     Longitude: 76.9142,
//     "Depth constructed (m)": 58.0,
//     "Tentative depth of installation of DWLR (m)": 25,
//     "Depth from ground measurement": "e",
//     "DWLR SR NO": "AAXI068",
//     Status: "completed",
//   },
//   {
//     "Zone wise Numbering": 17,
//     "  State  ": "Delhi",
//     "District ": "West",
//     Block: "PATELNAGAR",
//     location: "PUSA (NRL) Pz",
//     Latitude: 28.6392,
//     Longitude: 77.1622,
//     "Depth constructed (m)": 48.0,
//     "Tentative depth of installation of DWLR (m)": 45,
//     "Depth from ground measurement": "e",
//     "DWLR SR NO": "AAXI056",
//     Status: "Completed ",
//   },
//   {
//     "Zone wise Numbering": 18,
//     "  State  ": "Delhi",
//     "District ": "West",
//     Block: "PATEL NAGAR",
//     location: "Janakpuri Pz",
//     Latitude: 28.63,
//     Longitude: 77.09138888888889,
//     "Depth constructed (m)": 10.05,
//     "Tentative depth of installation of DWLR (m)": 20,
//     "Depth from ground measurement": 7.5,
//     "DWLR SR NO": "AAXI125",
//     Status: "Completed ",
//   },
//   {
//     "Zone wise Numbering": 19,
//     "  State  ": "Himachal pradesh",
//     "District ": "Bilaspur",
//     Block: "Ghumarwin",
//     location: "Goyal",
//     Latitude: 31.4475,
//     Longitude: 76.631389,
//     "Depth constructed (m)": NaN,
//     "Tentative depth of installation of DWLR (m)": 16,
//     "Depth from ground measurement": ".98 M",
//     "DWLR SR NO": "AAXI140",
//     Status: "Completed ",
//   },
//   {
//     "Zone wise Numbering": 20,
//     "  State  ": "Himachal pradesh",
//     "District ": "Hamirpur",
//     Block: "Hamirpur",
//     location: "Neri Collage",
//     Latitude: 31.69662,
//     Longitude: 76.469539,
//     "Depth constructed (m)": NaN,
//     "Tentative depth of installation of DWLR (m)": 50,
//     "Depth from ground measurement": "9.2 M",
//     "DWLR SR NO": "AAXI096",
//     Status: "Completed ",
//   },
//   {
//     "Zone wise Numbering": 21,
//     "  State  ": "Uttarakhand",
//     "District ": "Udham singh nagar",
//     Block: "Gadarpur",
//     location: "PipalyaNo.2",
//     Latitude: 29.0344,
//     Longitude: 79.2844,
//     "Depth constructed (m)": NaN,
//     "Tentative depth of installation of DWLR (m)": 50,
//     "Depth from ground measurement": "5.2 M",
//     "DWLR SR NO": "AAXI134",
//     Status: "Completed ",
//   },
//   {
//     "Zone wise Numbering": 22,
//     "  State  ": "Uttarakhand",
//     "District ": "Udham singh nagar",
//     Block: "Jaspur",
//     location: "Mahuadabra",
//     Latitude: 29.2803,
//     Longitude: 78.7991,
//     "Depth constructed (m)": NaN,
//     "Tentative depth of installation of DWLR (m)": 50,
//     "Depth from ground measurement": "15.2M",
//     "DWLR SR NO": "AAXI126",
//     Status: "Completed ",
//   },
//   {
//     "Zone wise Numbering": 23,
//     "  State  ": "Uttarakhand",
//     "District ": "Udham Singh Nagar",
//     Block: "Jaspur",
//     location: "Patrampur",
//     Latitude: 29.3273,
//     Longitude: 78.8691,
//     "Depth constructed (m)": NaN,
//     "Tentative depth of installation of DWLR (m)": 50,
//     "Depth from ground measurement": "20.2 M",
//     "DWLR SR NO": "AAXI149",
//     Status: "Completed ",
//   },
//   {
//     "Zone wise Numbering": 24,
//     "  State  ": "Uttarakhand",
//     "District ": "Udham Singh Nagar",
//     Block: "Kashipur",
//     location: "Shivlalpur, Amajhanda",
//     Latitude: 29.1631,
//     Longitude: 78.9131,
//     "Depth constructed (m)": NaN,
//     "Tentative depth of installation of DWLR (m)": 50,
//     "Depth from ground measurement": "20.1 M",
//     "DWLR SR NO": "AAxi129",
//     Status: "Completed ",
//   },
//   {
//     "Zone wise Numbering": 25,
//     "  State  ": "Uttarakhand",
//     "District ": "Udham Singh Nagar",
//     Block: "Khatima",
//     location: "Charubeta",
//     Latitude: 28.8895,
//     Longitude: 79.9352,
//     "Depth constructed (m)": NaN,
//     "Tentative depth of installation of DWLR (m)": 50,
//     "Depth from ground measurement": "9.8 M",
//     "DWLR SR NO": "AAXI009",
//     Status: "Completed ",
//   },
//   {
//     "Zone wise Numbering": 26,
//     "  State  ": "Uttarakhand",
//     "District ": "Udham Singh Nagar",
//     Block: "Khatima",
//     location: "Mohmmadpur Bhuria",
//     Latitude: 28.8767,
//     Longitude: 79.8526,
//     "Depth constructed (m)": NaN,
//     "Tentative depth of installation of DWLR (m)": 50,
//     "Depth from ground measurement": "5.2 M",
//     "DWLR SR NO": "AAXI135",
//     Status: "Completed ",
//   },
//   {
//     "Zone wise Numbering": 27,
//     "  State  ": "Uttarakhand",
//     "District ": "Udham Singh Nagar",
//     Block: "Rudrapur",
//     location: "ANJhaSchool",
//     Latitude: 28.9625,
//     Longitude: 79.3885,
//     "Depth constructed (m)": NaN,
//     "Tentative depth of installation of DWLR (m)": 50,
//     "Depth from ground measurement": "10.8 M",
//     "DWLR SR NO": "AAXI054",
//     Status: "Completed ",
//   },
//   {
//     "Zone wise Numbering": 28,
//     "  State  ": "Uttarakhand",
//     "District ": "Udham Singh Nagar",
//     Block: "Sitarganj",
//     location: "Bijt i",
//     Latitude: 28.885,
//     Longitude: 79.7559,
//     "Depth constructed (m)": NaN,
//     "Tentative depth of installation of DWLR (m)": 50,
//     "Depth from ground measurement": "4.2 M",
//     "DWLR SR NO": "AAXI050",
//     Status: "Completed ",
//   },
// ];
