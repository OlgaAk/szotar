import { Text, View, StyleSheet } from 'react-native';

export default function WordScreen({navigation, route}) {
  const word = route.params.word
 
  return (
   <View style={styles.container}>
       
    <Text style={styles.title}>{word.word}</Text>
    
    <Text style={styles.paragraph} >{word.translations[0].value}</Text>
    
    <Text style={styles.paragraph}>{word.translations[0].example}</Text>
    
    <Text style={styles.paragraph}>{word.translations[0].synonym}</Text>
    
    <Text style={styles.paragraph}>{word.etymology}</Text>
    
    <Text style={styles.paragraph}>{JSON.stringify(word.inflection)}</Text>
        
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 8
  },
  title: {
    fontSize: 20,
    fontWeight: "bold",
    marginBottom: 12,
  },
  paragraph: {
    fontSize: 16
  }
})
