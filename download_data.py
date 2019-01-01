from __future__ import print_function

from zipfile import ZipFile
import glob
import os
import shutil
try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve

URLBASE = 'https://f001.backblazeb2.com/file/Backblaze-Hard-Drive-Data/{}'
DATA = [
     'data_2015','data_Q1_2016', 'data_Q2_2016', 'data_Q3_2016', 'data_Q4_2016',
	'data_Q1_2017', 'data_Q2_2017', 'data_Q3_2017', 'data_Q4_2017']



def main(output_dir='data'):
    filenames = DATA
    urls = [URLBASE.format(filename + '.zip') for filename in filenames]
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    i = 0
    for url, filename in zip(urls, filenames):
        output_file = os.path.join(output_dir, filename + '.zip')

        if os.path.exists(output_file):
            print("{} already exists".format(output_file))
            continue

        print("Downloading from {} ...".format(url))
        urlretrieve(url, filename=output_file)
        print("=> File saved as {}".format(output_file))
        print("Extracting files...")
        with ZipFile(output_file, "r") as zip_ref:
            out_dir = os.path.join(output_dir, filename)
            zip_ref.extractall(out_dir)

        print("=> Files extracted...")
        print("Combining files...")

        if filename == 'data_2015':
           extracted = glob.glob(out_dir + "/2015/" + "*.csv")
           with open(output_dir + '/' + filename + '.csv', 'w') as outfile:
               fname = extracted[0]
               with open(fname) as infile:
                   for line in infile:
                       outfile.write(line)

               for fname in extracted[1:]:
                   j = 0
                   with open(fname) as infile:
                       for line in infile:
                            if j:
                                outfile.write(line)
                            j += 1

        if filename in ['data_Q1_2016', 'data_Q2_2016', 'data_Q3_2016', 'data_Q4_2016']:
           extracted = glob.glob(out_dir + "/" + filename + "/" + "*.csv")
           with open(output_dir + '/' + filename + '.csv', 'w') as outfile:
               fname = extracted[0]
               with open(fname) as infile:
                   for line in infile:
                       outfile.write(line)

               for fname in extracted[1:]:
                   j = 0
                   with open(fname) as infile:
                       for line in infile:
                            if j:
                                outfile.write(line)
                            j += 1
        if filename in ['data_Q1_2017', 'data_Q2_2017', 'data_Q3_2017', 'data_Q4_2017']:
           extracted = glob.glob(out_dir + "/" + "*.csv")
           with open(output_dir + '/' + filename + '.csv', 'w') as outfile:
               fname = extracted[0]
               with open(fname) as infile:
                   for line in infile:
                       outfile.write(line)

               for fname in extracted[1:]:
                   j = 0
                   with open(fname) as infile:
                       for line in infile:
                            if j:
                                outfile.write(line)
                            j += 1
        print("=> Files combined...")
        shutil.rmtree(out_dir)
        os.remove(output_file)
        print("=> Extra files cleaned ...")
        i += 1

if __name__ == '__main__':
    test = os.getenv('RAMP_TEST_MODE', 0)

    if test:
        print("Testing mode, not downloading any data.")
    else:
        main()
