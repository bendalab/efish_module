def read_info_file(file_name):
    info = []
    root = {}
    with open(file_name, 'r') as f:
        lines = f.readlines()
        for l in lines:
            if not l.startswith("#"):
                continue
            l = l.strip("#").strip()
            if len(l) == 0:
                continue
            if not ": " in l:
                sec = {}
                root[l] = sec
            else:
                parts = l.split(': ')
                sec[parts[0].strip()] = parts[1].strip()
    info.append(root)
    return info


def get_subject_info(file_name):
    info = read_info_file(file_name)
    subject = info[0]['Subject:']['Identifier'] [1:-1]
    species = info[0]['Subject:']['Species'] 
    dataset = info[0]['Recording:']['Name'][1:-1]     
    date = info[0]['Recording:']['Date'][1:-1] 
    return subject, species, date, dataset