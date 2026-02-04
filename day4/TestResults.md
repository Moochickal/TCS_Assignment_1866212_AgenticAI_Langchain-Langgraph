# 📈 Assignment: AI-Powered Customer Support Agent - Test Results
**Date:** February 4, 2026  
**Model:** Qwen3:30b (Ollama)  
**Hardware:** NVIDIA RTX 5090 (32GB VRAM)

## 📋 Executive Summary Table
The following table summarizes the performance of the LangGraph agent across five distinct customer support scenarios. Each test validates the **Classification**, **KB Retrieval**, and **Escalation Logic**.

| Test ID | Scenario | Identified Topic | Urgency | Action Taken | Logic Justification |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **TC-01** | Password Reset | **Account** | Low | ✅ Auto-Reply | Found direct solution in KB; simple resolution. |
| **TC-02** | Double Charge | **Billing** | High | 🚀 Escalate | High-urgency financial issues require human audit. |
| **TC-03** | PDF Export Crash | **Bug** | Medium | 🚀 Escalate | Software bugs are complex and require engineering. |
| **TC-04** | Dark Mode Request | **Feature Req.**| Low | ✅ Auto-Reply | Informational response drafted; no escalation needed. |
| **TC-05** | API 504 Errors | **Tech Issue** | High | 🚀 Escalate | Critical production downtime; immediate escalation. |

---

## 🔍 Detailed Workflow Trace: TC-02 (Billing Issue)
*This trace demonstrates the internal state transitions of the LangGraph workflow.*

**Input Email:** > "URGENT: I just checked my bank statement and I was charged $199 twice for the same annual subscription! I need an immediate refund and an explanation."



### 1. Classification Node
* **Logic:** The LLM analyzed the intent and keywords.
* **Output:** `{"urgency": "High", "topic": "Billing"}`

### 2. Research (Knowledge Base) Node
* **Logic:** The agent performed a lookup on the `Billing` key in the mock database.
* **Result:** *"Subscription double charges are refunded within 3-5 days."*

### 3. Draft Response Node
* **Draft Output:** > "Dear Customer, I am very sorry for the inconvenience of the double charge. I have analyzed your request and can confirm that our policy is to process these refunds within 3 to 5 business days. Because this is an urgent billing matter, I am escalating this to our financial team to ensure it is resolved immediately."

### 4. Action & Routing Node
* **Logic:** The `router_logic` function identified `urgency == "High"`.
* **Decision:** `escalate`
* **Status:** Final state updated with `action: "escalate"`.

---

## ✅ Technical Validation Results

1. **State Consistency:** The `TypedDict` successfully carried data from `classify` through to the final `print` statement without data loss.
2. **Resource Efficiency:** By using `num_gpu=999` on the RTX 5090, inference time for the 30B model averaged <1.5 seconds per node.
3. **Escalation Accuracy:** The agent correctly differentiated between a simple account query (Auto-Reply) and a production-level technical failure (Escalate).
