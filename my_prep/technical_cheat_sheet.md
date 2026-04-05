# Data Science Technical Cheat Sheet: Akash Kumar

This cheat sheet is a targeted review of the concepts most relevant to your projects and common Data Science interview questions.

---

## 🔬 Machine Learning Fundamentals (OmniHealth AI Focus)

### SVM (Support Vector Machines)
- **Concept**: Finding the optimal hyperplane that maximizes the "margin" between classes.
- **Kernels**: Used for non-linear data (RBF, Polynomial). In Parkinson’s, RBF is likely used to handle complex vocal signatures.
- **Pros/Cons**: Excellent for high-dimensional data (like your 22 vocal features) but can be memory-intensive.

### Logistic Regression
- **Concept**: Uses the **Sigmoid function** ($\sigma(z) = \frac{1}{1+e^{-z}}$) to map linear inputs into a probability range (0 to 1).
- **Decision Boundary**: Usually 0.5, but in medical contexts, you might lower it to increase precision/recall for specific risks.

### Precision vs. Recall (The Medical Trade-off)
- **Precision**: "Of all predicted positive, how many were actually positive?" (Avoids false alarms).
- **Recall**: "Of all actually positive, how many did we catch?" (Avoids missing symptoms).
- **Your Project**: In **LiverSegNet**, **Recall is king** (Focal Tversky $\alpha=0.7$). You’d rather have a false alarm than miss a liver boundary during surgery.

---

## 🖼️ Computer Vision & UNet (LiverSegNet Focus)

### ResNet Encoders (ResNet34/50)
- **Residual Learning**: Uses "Skip Connections" to allow gradients to flow through deep networks without "vanishing."
- **Why it matters**: Allows you to train deep models (Model A: ResNet50) without losing the ability to learn basic textures.

### ASPP (Atrous Spatial Pyramid Pooling)
- **Concept**: Used in DeepLabV3+. Uses different "dilation rates" to look at an image multiple times.
- **Use Case**: Helps the model understand both "Small Vessels" and "Large Organs" simultaneously.

### U-Net Skip Connections
- **Concept**: Directly concatenates high-resolution features from the encoder to the decoder.
- **Why it matters**: Preserves the "sharpness" of tool edges, preventing them from becoming "blobs" during segmentation.

---

## 🧠 Deep Learning & Reasoning (MemReason Focus)

### Attention Mechanism
- **Formula**: $Attention(Q, K, V) = softmax(\frac{QK^T}{\sqrt{d_k}})V$
- **In MemNN**: It measures the "relevance" between the question (Q) and each sentence in the story (K). The most relevant sentences (V) are weighted more heavily in the output.

### Weight Tying
- **Concept**: Sharing weights between different layers (Input vs. Output embeddings).
- **Benefit**: Reduces the model's footprint and acts as a form of regularization (preventing it from "memorizing" specific words instead of learning meanings).

---

## 🐍 Python & Tools

### Streamlit Session State
- **Problem**: Streamlit reruns the whole script on every interaction (variables are lost).
- **Solution**: `st.session_state` allows variables to persist across reruns (essential for your patient history log).

### PyTorch Autograd
- **Concept**: Automatically calculates gradients for all operations in the "Forward Pass."
- **`optimizer.zero_grad()`**: Crucial to call before every backprop step to clear gradients from the previous batch.

---

## 📊 Metrics to Remember (Interview Proof yourself)

| Metric | **Definition** | **Where you used it** |
| :--- | :--- | :--- |
| **mIoU (Mean Intersection over Union)** | Measures the overlap between predicted mask and ground truth. | **LiverSegNet**: Tracked the accuracy of Liver/Tool masks. |
| **F1-Score (Dice Coefficient)** | Harmonic mean of precision and recall. Strong for imbalanced data. | **MemReason**: Used to evaluate the accuracy of "Answer Extraction." |
| **Precision** | $\frac{TP}{TP+FP}$ (Focus on "False Alarms"). | **OmniHealth AI**: Ensuring "Healthy" people aren't misdiagnosed. |
| **Recall (Sensitivity)** | $\frac{TP}{TP+FN}$ (Focus on "Missing a piece"). | **LiverSegNet**: Crucial to ensure tissue is never missed. |

---

## ⚙️ Hyperparameter Tuning Cheat-Sheet

### Grid Search vs. Random Search
- **Grid Search**: Exhaustive search through every combination of parameters (Guarantees best).
- **Random Search**: Randomly samples the parameter space (Much faster, often finds global optima).
- **In your projects**: You likely used **Adaptive Learning Rates (OneCycleLR)** in `train_pipeline.py`.

### Focal Tversky Loss Parameters
- **$\alpha=0.7$**: Recall penalty (Focus on FN).
- **$\beta=0.3$**: Precision penalty (Focus on FP).
- **$\gamma=1.33$**: Focal power (Focus on Hard Pixels).
