# NJ Real Estate Data CSV

This repository contains a CSV file storing data regarding New Jersey real estate listings. The file is designed for structured analysis and debugging, utilizing a `~` delimiter.

---

## 📂 File Format

The CSV file is structured as follows:

| Column Index | Column Name                  | Description                                                                                                                                          |
|--------------|------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0            | `photo links`               | Links to images of the property.                                                                                                                     |
| 1            | `price`                     | Price of the property.                                                                                                                               |
| 2            | `address`                   | Address of the property.                                                                                                                             |
| 3 to 58      | `features`                  | Contains strings representing several features under specific categories. Each feature is separated by ||.                                          |
| 59           | `zillow link to property`   | URL linking to the specific property on Zillow.                                                                                                      |
| 60           | `zillow link to initial search` | URL linking to the original search for debugging purposes.                                                                                            |

---

## 📝 Key Notes

### **Features Column**
- Each feature column contains a string with multiple attributes categorized by a title.
- Features are separated by `||` for easy parsing.

#### **Example:**
```plaintext
bedrooms & bathrooms||bedrooms: 1||bathrooms: 1||full bathrooms: 1


Link to images
https://drive.google.com/drive/folders/1I7FhX47G1_M62_o5N_Suc0QsZsQ7Dqc-?usp=drive_link
(note: all imgs are named {pd_index}_{num}.jpg) 
