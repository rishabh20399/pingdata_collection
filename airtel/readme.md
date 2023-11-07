1. First fork the repo into your account, then clone that forked repository on termux in mobile
```
git clone git@github.com:username/pingdata_collection.git

```
Replace "username" with your username</br>
  </br>
2. Run test.sh first to ensure that everything runs smoothly on your side
```
cd pingdata_collection
git fetch --all
git reset --hard origin/main
cd airtel
chmod +x test.sh
./test.sh
```
Replace "main" with your branch name.
