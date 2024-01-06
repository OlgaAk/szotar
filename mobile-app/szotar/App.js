import {NavigationContainer} from '@react-navigation/native';
import {createNativeStackNavigator} from '@react-navigation/native-stack';

import {WordScreen} from '.WordScreen'
import {HomeScreen} from '.HomeScreen'

const Stack = createNativeStackNavigator();

export default function App() {
 
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen
          name="Home"
          component={HomeScreen}
          options={{title: 'Szotar'}}
        />
        <Stack.Screen name="Word" component={WordScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

