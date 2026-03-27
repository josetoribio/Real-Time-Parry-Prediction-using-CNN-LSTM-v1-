# 🥋 Parry Timing Detection (CNN + LSTM)

## 📌 Overview

A **parry** in *Street Fighter III: 3rd Strike* is a defensive mechanic that allows a player to negate an opponent’s attack with zero blockstun by tapping toward the opponent at the correct moment.

A **projectile** is any attack that creates a moving hitbox separate from the character, such as Ryu’s Hadoken.
<img width="1600" height="700" alt="frame_00001" src="https://github.com/user-attachments/assets/220586f1-93c2-469b-92b7-d379d09e283d" />


This project explores using deep learning to predict the **correct timing window to parry a projectile** based on sequences of frames.

---

## ⚙️ Tech Stack

* Python
* PyTorch
* CNN + LSTM architecture
* PIL / OpenCV (image processing)

---

## 🧠 Model Architecture (V1)

* A **CNN** extracts visual features from each frame
* An **LSTM** processes sequences of frames to learn motion over time
* Final output:

  * `0 → no_parry`
  * `1 → parry`

---

## 📊 Dataset Approach (V1)

The dataset was initially structured using folder-based labels:

* `no_parry/` → startup frames
* `parry/` → frames near impact

Sequences of frames were generated and used as input to the model.

---

## ⚠️ Key Limitation

The model learned to distinguish **early vs late frames**, rather than identifying the **precise timing window** required for a successful parry.

This revealed a critical issue:

> Folder-based labeling is insufficient for time-sensitive decision tasks.

Because the dataset lacked **mid-flight and timing-aware labels**, the model failed to learn *when* to act—only *what phase* it was seeing.

---

## 🔄 Future Improvements

* Transition to **time-based labeling** instead of folder-based labels
* Include full projectile lifecycle:

  * startup
  * mid-flight
  * approach
  * parry window
  * late frames
* Increase sequence length for better temporal understanding
* Incorporate **velocity and distance tracking** of the projectile

---

## 🚀 Goal

Build a model capable of predicting:

> “Is *this exact moment* the correct time to parry?”

---

## 📁 Project Structure

```
scripts/
  model.py
  dataset_loader.py
  train.py
```

---

## 🧩 Status

Version 1 complete — demonstrated core pipeline and identified dataset limitations.
Next iteration will focus on **temporal labeling and improved timing accuracy**.
