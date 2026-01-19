 Grade RAG Service

A backend service for  evaluating Retrieval-Augmented Generation (RAG) systems   by scoring retrieval quality, response correctness, and robustness under adversarial or edge-case inputs.

The goal of this project is to make RAG systems   measurable, reproducible, and debuggable  , rather than treating them as black boxes.

---

 What this service does

Grade RAG Service orchestrates RAG evaluations by:
- Running controlled retrieval + generation workflows
- Scoring results using deterministic and heuristic metrics
- Capturing full metadata for repeatable analysis

It is designed to answer practical questions like:
- Did retrieval actually help the response?
- How stable are results across retries?
- Where does the pipeline degrade under adversarial inputs
