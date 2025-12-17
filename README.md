# FLINT

## Usage

Follow these steps to run the tool:

1. **Run `main.py`**: Execute the main script to start the program.

   ```
   python main.py
   ```

2. **Input Prompts**: After running the script, you will be prompted to enter the following information:

   - **Pcap file path**: The full path to your pcapng file.
   - **Protocol name**: The name of the protocol you want to analyze (e.g., coap).
   - **Output txt file path**: The full path where the output text file will be saved.

   The program will guide you through each input step interactively.

## Example

Here is an example of how to respond to the prompts based on your provided example:

```
# When prompted, enter the following:
Pcap file path: ../dataset/coap.pcapng
Protocol name: coap
Output txt file path: ../dataset/coap.txt
```

This will process the `coap.pcapng` file for the CoAP protocol and save the results to `coap.txt`.

