Thank you for the clarification! Here’s the updated **README** that reflects the measurements for the **inner and outer diameters of the dryer** instead of a general circle:

---

# Dryer Diameter Measurement Project

This project uses **OpenCV** to measure the **outer and inner diameters** of the dryer openings in images. The process involves **ORB feature matching** and **Homography** for image registration, extracting the circular regions from the images, and calculating the diameters of these openings. The results are displayed on the image and saved to an Excel file for further analysis.

## Requirements

1. Python 3.x
2. OpenCV
3. NumPy
4. Pandas
5. Excel (for saving measurements)

To install the required Python libraries, run the following commands:

```
pip install opencv-python numpy pandas
```

## Project Structure

```
/project
    /images           # Folder for images
    crop.py           # Python script for diameter extraction
    dryers.xlsx       # Excel file for saving measured diameters
    README.md         # This file
```

### Step-by-Step Guide

1. **Extract the ZIP File**:
   After downloading the project, extract the contents of the ZIP file to a folder of your choice.

2. **Place Images in the 'images' Folder**:
   Inside the project folder, you will find a folder named `images`.
   Place the images you want to process in this folder.
   Make sure the images show the dryer openings you want to measure.

3. **Edit the Code for Your Image**:
   Open the `crop.py` file.
   In this file, locate the section where the dryer’s **coordinates** and **radius** are defined:

   ```python
   xc_ref, yc_ref, r_ref = 300, 166, 33
   ```

   * `xc_ref, yc_ref`: These are the **coordinates** of the center of the opening in the reference image.
   * `r_ref`: This is the **radius** of the opening in the reference image.

   You need to update these values based on your dryer image:

   * For example, use an image viewer to find the center and radius of the dryer opening in your reference image and update the values in the code accordingly.

4. **Image Registration (ORB and Homography)**:
   The **image registration** process aligns two images (reference and target) using feature matching and homography. The steps involved are:

   * **ORB Feature Matching**:
     The **ORB (Oriented FAST and Rotated BRIEF)** algorithm detects key points in the reference image and the target image, then matches the key points between the two images.

   * **Homography Calculation**:
     After matching the key points, the homography matrix is computed to transform the target image's coordinates into the reference image’s coordinate system. This helps to align the target image with the reference image.

   This process is crucial for accurately calculating the transformed coordinates of the dryer opening in the target image.

5. **Run the Script**:
   After setting up your reference image and coordinates, run the `crop.py` script to crop the dryer opening from the target image and calculate the **outer and inner diameters**:

   ```bash
   python crop.py
   ```

   The script will:

   * Detect the outer and inner diameters of the dryer opening.
   * Print the diameters (in pixels) in the terminal.
   * Display the target image with the diameters annotated.
   * Save the results in an Excel file (`dryers.xlsx`).

6. **Saving Results**:
   The measured **outer diameter (OD)** and **inner diameter (ID)** of the dryer opening will be saved to the `dryers.xlsx` file. You can open the Excel file to view the measurements for each processed image.

---

### Explanation of Core Functions

1. **ORB Feature Matching**:
   ORB is a fast and efficient method for feature detection and matching in images. It finds distinctive keypoints in both the reference and target images and matches them. The good matches are then used to calculate the **homography matrix**, which aligns the images and allows for accurate measurement of the diameters.

2. **Homography**:
   Homography is a transformation technique that maps the points from one image to another. In this project, it helps align the reference and target images, allowing for accurate measurement of the dryer opening’s diameters in the target image.

3. **Diameter Calculation**:
   After isolating the dryer opening from the image, the code calculates the **outer** and **inner diameters** using contour detection and the minimum enclosing circle.

4. **Saving Data to Excel**:
   The measurements are written to an Excel file for future analysis or reporting. The file `dryers.xlsx` will contain the **outer diameter (OD)** and **inner diameter (ID)** for each image processed by the script.

---

## Conclusion

This project is designed for measuring the **outer and inner diameters of dryer openings** in images. By using OpenCV’s feature matching and homography, the project achieves accurate measurements. The results are saved in an Excel file for easy access and further analysis.

Feel free to modify the script or add new functionality as needed!
