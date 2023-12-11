import os

cwd = os.getcwd()
fs = os.listdir( cwd )
apk_path = None
for f in fs:
    path = os.path.join(cwd, f)
    if os.path.isfile(path) and path.endswith('.apk'):
        apk_path = path
        break

if apk_path == None:
    print('1. Some systems do not support drag and drop, which requires manual input.')
    print('2. Placing the installation package (APK) in the current directory also works')
    apk_path = input("drag in apk:\n")
    apk_path = apk_path.replace('\\','/')

import zipfile
if not zipfile.is_zipfile(apk_path):
    raise

z = zipfile.ZipFile(apk_path)

import tempfile
tempdir = tempfile.TemporaryDirectory()

meta_path = os.path.join(tempdir.name,'metadata')
so_path = os.path.join(tempdir.name,'lib')
z.extract('assets/bin/Data/Managed/Metadata/global-metadata.dat', path=meta_path, pwd=None)
z.extract('lib/arm64-v8a/libil2cpp.so',path=so_path,pwd=None)

real_meta_path = os.path.join(meta_path,'assets/bin/Data/Managed/Metadata/global-metadata.dat')
real_so_path = os.path.join(so_path,'lib/arm64-v8a/libil2cpp.so')

if not os.path.exists("./dest"):
    os.makedirs('./dest')
dumper_path = os.path.join(os.getcwd(),'dumper/Il2CppDumper.exe')

try:
    os.system(f'{dumper_path} {real_so_path} {real_meta_path} dest')
except Exception as e:
    print(e)