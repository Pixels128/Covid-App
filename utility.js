import AsyncStorage from '@react-native-async-storage/async-storage';

const uuid = require('uuid');

if (__DEV__ && typeof global.crypto !== 'object') {
    global.crypto = {
        getRandomValues: (array: any[]) => array.map(() => Math.floor(Math.random() * 256)),
    };
}

const regenerateUUID = async () => {
    try {
        let newUuid = uuid.v4()
        await AsyncStorage.setItem("UUID", newUuid)
        console.log("New UUID", newUuid)
    }
    catch (error) {
        console.log(error)
    }
}

const storeUser = async () => {
    try {
        const savedUser = await AsyncStorage.getItem("UUID");
        if (savedUser == null) {
            console.log("UUID not found, regenerating...")
            regenerateUUID()
        }
        console.log("success")
    } catch (error) {
        console.log("Error:", error);
    }
    getUser()
};
const getUser = async () => {
    try {
        const savedUser = await AsyncStorage.getItem("UUID");
        console.log("Is Stored:", savedUser);
    } catch (error) {
        console.log(error);
    }
};

const getUserUUID = async () => {
    const userID = await AsyncStorage.getItem("UUID");
    return userID
}
storeUser()

const getAndReportUser = async () => {
    const savedUser = await AsyncStorage.getItem("UUID");
    report(savedUser)
}

export default function requestEnableBLE() {
    console.log(1)
}

function report(userID) {
    const x = 1
    const TCPIP = '10.208.2.61:5000'
    var xhr = new XMLHttpRequest();
    console.log('http://' + TCPIP + '/api/v2/' + userID + '?hasCovid=true')
    xhr.open("POST", 'http://' + TCPIP + '/api/v2/' + userID + '?hasCovid=true', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        "hasCovid": true
    }));
    console.log("Report Sent id:", userID)
}

const numCovidContacts = 1
