import csv

def save_csv(mydict,fileName):
    headers = []
    vals    = []
    for key,val in mydict.items():
        headers += [key]
        vals    += [val]

    N = len(vals[0])
    with open(fileName,'w',newline='') as f:
        w = csv.writer(f)
        w.writerow(headers)
        for i in range(N):
            row = [f[i] for f in vals]
            w.writerow(row)


def load_csv(fileName):
    my_dict = {}
    with open(fileName,mode='r') as infile:
        reader = csv.reader(infile)
        row_count = 0
        for row in reader:
            if row_count==0:
                keys = row

            else:
                for key,it in zip(keys,row):
                    if row_count==1:
                        my_dict[key] = [it]
                    else:
                        my_dict[key] += [it]
            row_count+=1


    return my_dict
