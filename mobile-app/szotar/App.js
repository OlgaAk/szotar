import {NavigationContainer} from '@react-navigation/native';
import {createNativeStackNavigator} from '@react-navigation/native-stack';

import WordScreen from './WordScreen'
import HomeScreen from './HomeScreen.js'

const Stack = createNativeStackNavigator();

export default function App() {
 
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen
          name="HomeScreen"
          component={HomeScreen}
          options={{title: 'Dictionary'}}
        />
        <Stack.Screen name="WordScreen" component={WordScreen} options={{title: ''}}/>
      </Stack.Navigator>
    </NavigationContainer>
  );
}

