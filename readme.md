This template requires credentials from:
1) Mongodb.com
2) Google OAuth - https://console.cloud.google.com/apis/dashboard
3) OpenStreetMaps - just need to add MY_EMAIL_ADDRESS to your secrets.py file

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/conchesness/CCPA2)

https://deploy.cloud.run/?git_repo=https://github.com/conchesness/CCPA2

Embedded doc cheatsheat
Create
Obj.embeddedobjfiled.create(
    embeddeddocfield,
    ...
)
obj.save()

Update
obj.embeddedObjField.filter(oid=objid).update(
    embeddeddocfield,
    ...
)
obj.save()

Delete
    obj.embeddedObjField.filter(oid=adultoid).delete()
    obj.save()

Get/Read one
    embeddedObj = obj.embeddedObjField.get(oid=objectid)