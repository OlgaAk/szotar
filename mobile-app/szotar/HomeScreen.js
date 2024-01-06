import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View, FlatList, TextInput } from 'react-native';
import {useState} from 'react';
import data from './definitions.json'

export default function App() {
  const [text, setText] = useState('');
  const [wordList, setWordList] = useState(data);
  
  const onInputChanged = newText => {
     console.log('hello')
    setText(newText)
    console.log(newText)
    if(newText) {
      setWordList(data.filter(item => item.word.startsWith(newText.toLowerCase())))
    } else {
    setWordList(data)
    }
  }
  
  return (
   <View style={styles.container}>
  
   <View style={styles.textInputContainer}>
   
    <TextInput
          style={styles.textInputStyle}
          placeholder="Type here to find a word!"
          onChangeText={onInputChanged}
          defaultValue={text}
        />
        
    </View>
      
    <View style={styles.listContainer}>
  
      <FlatList
        data={wordList}
        renderItem={({item}) => <Text style={styles.word}>{item.word}</Text>}
      />
    
      <StatusBar style="auto" />
    </View>
    
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    justifyContent: 'center',
    padding: 8,
    marginTop: 60
  },
    listContainer: {
    flex: 3,
    alignItems: 'left',
    justifyContent: 'center',
    padding: 8
  },
  textInputContainer: {

  },
  textInputStyle: {
    borderWidth: 1,
    borderColor: "#ccc",
    height: 40,
    borderRadius: 8,
    marginRight: 30
  },
  word: {
    fontSize: 20,
    paddingBottom: 8,
  }
});
