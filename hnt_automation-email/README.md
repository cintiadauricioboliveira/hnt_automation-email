
# VTEX Email Trigger Automation

This script automates the process of triggering emails through the VTEX platform. It reads from a `configs.json` file for account details, authenticates with the VTEX API, reads specific template folders, modifies the email address in the respective JSON files, and sends a request to the VTEX mail service.

## Requirements
- Python 3+
- Libraries: `requests`, `tqdm`

To install the required libraries, run:
```
pip install requests tqdm
```

## Usage

1. Modify the `configs.json` file with the appropriate values for your VTEX account:
```json
{
    "account": "YourVtexAccount",
    "X-VTEX-API-AppToken": "YourAppToken",
    "X-VTEX-API-AppKey": "YourAppKey",
    "template-name": [
        "template1",
        "template2",
        "template3"
    ]
}
```

2. Place your JSON files inside folders that match the names specified in the "template-name" list in `configs.json`. For example, for "template1", there should be a folder named "template1" containing the relevant JSON files.

3. Run the script:
```
python your_script_name.py
```

4. When prompted, enter the target email address. The script will then process each template, update the email address in the JSON files, and send a request to the VTEX platform.

## Adding New Templates

To validate new templates:

1. Find in VTEX Message Center the template name you are looking for:
![Template name](/readme/image.jpg)
2. Add the new template name to the "template-name" list in `configs.json`.
3. Create a folder in the script directory with the same name as the new template. This folder should contain all the relevant JSON files for that template.
4. Run the script as usual. It will automatically detect and process the new template folder.

Para executar o comando
python email-sender.py
python3 email-sender.py
