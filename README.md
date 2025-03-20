
#Event Log Extraction for Process Mining Using Large Language Models

## Overview

### Empowering Data Exploration with Ease

Process mining is a discipline that enables organizations to discover and analyze their work processes. A prerequisite for conducting a process mining initiative is the so-called event log, which is not always readily available. In such cases, extracting an event log involves various time-consuming tasks, such as creating tailor-made structured query language (SQL) scripts to extract an event log from a relational database. With this work, we investigate the use of large language models (LLMs) to support event log extraction, particularly by leveraging LLMs ability to produce SQL scripts.
This web application enables users to upload their own database or choose from sample example database, fostering an intuitive and seamless exploration experience.

Developed by researchers from <strong>Kühne Logistics University</strong>, this tool serves as a solid foundation for event log generation, allowing users to ask targeted questions and receive real-time responses.

---

## Technical Details

### Prerequisites

- **Python Version**: The application requires Python 3.10.15
- **Dependencies**: All required dependencies are listed in the `requirements.txt` file.

### Getting Started

1. Clone the repository to your local machine:
   ```bash
   git clone ...
   cd ...
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

5. Open the provided local URL in your browser to start using the chatbot.


---


## Contact

For inquiries or support, please contact:
- **Email**: [kiran.busch@klu.org]