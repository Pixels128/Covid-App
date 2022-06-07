import { StatusBar } from "expo-status-bar";
import { StyleSheet, Text, View } from "react-native";
import { SafeAreaView, Button } from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { AppRegistry } from "react-native";
import { BleManager } from "react-native-ble-manager";

AppRegistry.registerComponent("MyAwesomeApp", () => App);

BleManager.start({ showAlert: false }).then(() => {
  // Success code
  console.log("Module initialized");
});

const uuid = require("uuid");

if (__DEV__ && typeof global.crypto !== "object") {
  global.crypto = {
    getRandomValues: (array: any[]) =>
      array.map(() => Math.floor(Math.random() * 256)),
  };
}

const regenerateUUID = async () => {
  try {
    let newUuid = uuid.v4();
    await AsyncStorage.setItem("UUID", newUuid);
    console.log("New UUID", newUuid);
  } catch (error) {
    console.log(error);
  }
};

const storeUser = async () => {
  try {
    const savedUser = await AsyncStorage.getItem("UUID");
    if (savedUser == null) {
      console.log("UUID not found, regenerating...");
      regenerateUUID();
    }
    console.log("success");
  } catch (error) {
    console.log("Error:", error);
  }
  getUser();
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
  return userID;
};
storeUser();

const getAndReportUser = async () => {
  const savedUser = await AsyncStorage.getItem("UUID");
  report(savedUser);
};

function requestEnableBLE() {
  console.log(1);
}

function report(userID) {
  const x = 1;
  const TCPIP = "10.208.2.61:5000";
  var xhr = new XMLHttpRequest();
  console.log("http://" + TCPIP + "/api/v2/" + userID + "?hasCovid=true");
  xhr.open(
    "POST",
    "http://" + TCPIP + "/api/v2/" + userID + "?hasCovid=true",
    true
  );
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send(
    JSON.stringify({
      hasCovid: true,
    })
  );
  console.log("Report Sent id:", userID);
}

let numCovidContacts = 1;

export default function App() {
  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.textStyle}>
        {numCovidContacts} Close Contact Covid Cases
      </Text>
      <Text>{"\n"}</Text>
      <Button
        onPress={requestEnableBLE}
        title="Bluetooth Disconnected"
      ></Button>
      <Text>{"\n"}</Text>
      <Button onPress={regenerateUUID} title="Regenerate Unique ID"></Button>
      <Text>{"\n"}</Text>
      <Button
        color="#f00"
        onPress={getAndReportUser}
        title="Report having Covid-19"
      ></Button>
      <StatusBar style="auto" />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
  },
  textStyle: {
    fontSize: 24,
  },
});

// ##########################################################################################################
// ##########################################################################################################
// ##########################################################################################################
// ##########################################################################################################
// ##########################################################################################################
// ##########################################################################################################
// ##########################################################################################################
// ##########################################################################################################
