Attempt to parse the 510(k) Summary documents for devices on the FDA's [AI-Enabled Medical Devices List](https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-enabled-medical-devices), searching for certain keywords to gauge interest / lack of interest in certain pathologies, modalities, and demographics.

Currently only parses the Summary PDF of 510(k) submissions (Submission Number K######). Classification Order and Decision summary could be added for De Novo devices.
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
### Modifications
Specify product codes of interest (set to empty list if parsing all) and naming variables
```python
product_codes = ['QAS', 'QBS', 'QDQ', 'QFM']
custom_flag = 'Peds_Flag'
save_name = 'list_with_peds_CAD_codes.xlsx'
```

Modify regex for search parameters. Example below for pediatric indications:
```python
# search Summary PDF for specific terms (NLP w/ LLM could be used here in place of regex)
if re.findall(r" pediatric|children", text, re.IGNORECASE):
    hit_count[index] = 1
else: hit_count[index] = 0

# search for a more specific regex and override to 0 if not intended
if re.search(r'\bnot intended\b(?:\W+\w+){1,5}?\W+\bpediatric\b', text, flags=re.IGNORECASE) is not None:
    print(str(index)+'/'+str(len(df))+': '+k_number + ', explicitly not intended')
    hit_count[index] = -1

if hit_count[index] == 1:
    print(str(index)+'/'+str(len(df))+': '+k_number + ' likely intended for pediatric or children')
elif hit_count[index] == 0:
    print(str(index)+'/'+str(len(df))+': '+k_number + ', no mention')
```
