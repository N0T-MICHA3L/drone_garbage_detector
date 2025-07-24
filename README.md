## 🌍 Project Overview: **AI-Based Coastal Trash Detection and Heatmap Visualization**

### 📌 **Introduction: drone_garbage_detector** 

This system leverages drone video footage and artificial intelligence (AI) to automatically detect and visualize coastal garbage. It presents the distribution of trash on an interactive heatmap, offering a valuable tool for environmental monitoring and coastal cleanup planning.
As the name suggests, this is a drone garbage detecting software that was developed in the aim of reducing the number of garbage on beaches and rivers. Once a a footage of a drone garabage is uploaded, this software will pin and label all the locations of the trash the software is able to detect on a map. In this spirit, people can use this generated map to identify and cleanup trashes on becahes, rivers, or other landscapes. 

---

### 🧭 **System Workflow**

![image](https://hackmd.io/_uploads/H1iyG2RUle.png)


1. **Drone Filming**

   * A drone captures aerial video footage along the coastline, recording both visual and GPS data.

2. **Data Extraction**

   * The **flight log** is processed to extract GPS location data using [PhantomHelp Log Viewer](https://www.phantomhelp.com/logviewer/).
   * The **video file** is analyzed using an AI model trained to detect beach garbage:
     🔗 [Beach Garbage Detection Model on Roboflow](https://universe.roboflow.com/litter-beach-detection/beach-garbage/model/1)
     - examples：Trash detected by the AI model is highlighted with purple bounding boxes.
     ![frame_745](https://hackmd.io/_uploads/BkQqXhC8gx.jpg)
     ![frame_356](https://hackmd.io/_uploads/Hy5VX20Ill.jpg)
     ![frame_633](https://hackmd.io/_uploads/SJrUm3A8ex.jpg)

     

3. **Analysis Program**

   * The AI model identifies trash in the video frames and matches them with corresponding GPS coordinates based on timestamps.
   * This generates structured geographic data of trash locations and density.

4. **Heatmap Visualization**

   * Detected garbage locations are plotted on an interactive map using Leaflet and heatmap visualization techniques.
   * Each trash hotspot is represented by color intensity corresponding to trash concentration.
   * The heatmap page can be viewed in a browser for real-time exploration and monitoring.
  
![image](https://hackmd.io/_uploads/Bkn4f308xe.png)


---

### 🌐 **Features**

* **AI Detection**: Automated trash recognition using deep learning.
* **Geospatial Mapping**: Each detection is geo-referenced using drone flight logs.
* **Heatmap View**: Trash density is visualized on a live map with zoom and pan features.
* **Environmental Application**: Supports environmental agencies, researchers, and community clean-up efforts.

---

### 🛠️ **Technologies Used**

| Component       | Tool/Technology                                    |
| --------------- | -------------------------------------------------- |
| AI Model        | Roboflow Beach Garbage Detection                   |
| Drone Hardware  | Any GPS-enabled UAV (e.g., DJI Phantom, Mavic)     |
| GPS Extraction  | [PhantomHelp Log Viewer](https://phantomhelp.com)  |
| Web Map         | Leaflet.js + Leaflet.heat plugin                   |
| Data Processing | Custom Python / JS scripts for syncing video & GPS |

---

### 📈 **Use Cases**

* Coastal environmental surveys
* Marine pollution hotspot identification
* AI-assisted shoreline clean-up planning
* Educational or citizen science platforms

---

### 🧾 **Future Enhancements**

* Real-time drone video + GPS syncing
* Integration with environmental reporting dashboards
* Multi-date comparison for trend analysis

---
- Michael Lin 
