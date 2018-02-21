import yaml

fh = open('settings.yaml')
a = yaml.load(fh)

for b in a:
    print(a[b]['check'])
