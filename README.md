## Bitwarden Password Deduper

Bitwarden Password Deduper is a simple python script intended to dedupe entries from Bitwarden.

This is specifically useful if you migrate from multiple password managers into Bitwarden and end up with tons of duplicates.

Inspired by the following reddit thread: https://www.reddit.com/r/Bitwarden/comments/aon967/bitwarden_duplicate_entries_remover/

### How to use

#### Prerequisites

First of all, you will need python3. You can check whether you have it installed by the following command:
```bash
which python3
```

If it shows `/usr/bin/python3`, you are good to go.

If different value shows up, either change first line of `deduper.py` to `#! [output from 'which']` or just use the following command:

```bash
python3 deduper.py [path_to_our_exported_csv_file]
```

#### Export Bitwarden vault

Sign in to the website, then go to `Tools` > `Export Vault`. Select `.csv` as the file format and save it to the same folder as the script.

#### Run the script

* Open a terminal and cd to that folder.
* Make the script executable on Linux/Mac with chmod +x `deduper.py`. (Windows doesn't need that).
* Then run the script with the name of your export as a command line argument. For example:

```bash
./deduper.py bitwarden_export_20190208123456.csv
```

or

```bash
python3 deduper.py bitwarden_export_20190208123456.csv
```

You will end up with 2 more files in the same folder:

* `bitwarden_export_20190208123456_deduped.csv` - contains clean, deduped file, which is ready to be imported back to Bitwarden.
* `bitwarden_export_20190208123456_removed_entries.csv` - contains all removed duplicate entries.

#### Clear old data on the website

After previewing your `.csv` files to make sure you really do have your data there, go to `My Vault`, click the gear icon, then `Select All`. Then the gear icon again and `Delete Selected`.

#### Annoying (Optional) Step

On the left of your Vault, you have some folders. If you don't delete those manually, you will end up with duplicated folders.

In order to delete those:

1. Click on folder name. Pen symbol should appear at the end of the line.
2. Click on the pen symbol. Small window pops up.
3. Click trash icon to delete the folder.
4. Repeat steps `1.` to `3.` for each folder you have.

#### Import your cleaned vault

Import the `*_deduped.csv` file under `Tools` > `Import Data` and choose `Bitwarden (csv)` format. Select your file and click `Import Data`.

Done!

#### Disclaimer

I'm not responsible if this blows up your computer or you lose all your passwords. It's a quick and dirty "thing you will use once and then throw away".

Hope it helps someone.
