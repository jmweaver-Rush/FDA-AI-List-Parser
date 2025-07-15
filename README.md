Attempt to scrape the FDA's [AI-Enabled Medical Devices List](https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-enabled-medical-devices) for certain keywords to gauge interest / lack of interest in certain pathologies, modalities, and demographics.

Currently only parses the Summary PDF of 510(k) submissions (Submission Number K######).
<img width="694" height="493" alt="image" src="https://github.com/user-attachments/assets/d490db90-339f-4c9a-92dc-cc3aa1dd48df" />

510(k) Summary documents are not standardized which makes parsing for specific information nontrivial. Broadly searching for key words (in this example 'pediatric') will likely overestimate the number of devices indicated for pediatric use as the Summary document may mention pediatric in the context of a predicate device, but not necessarily the subject device. Therefore, an LLM for NLP may be more effective in correctly classifying these devices.

### Installation
`pip install -r requirements.txt`

### Usage
```python
# Download .xlsx file if not in repository:
# https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-enabled-medical-devices
python main.py # modify regex for key word searching
# outputs new .xlsx
```
