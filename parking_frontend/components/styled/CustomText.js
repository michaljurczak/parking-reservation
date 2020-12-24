import React from 'react';
import { Text } from 'react-native'; 

import CenterView from './CenterView';

/**
 * Component for wrapping another component with app style - centers the text.
 * @param {string} text Any string allowed 
 * @return {CustomText} Returns styled View which centers the text in the component.
 */

const customText = props => {
  return (
    <CenterView>
      <Text>{props.text}</Text>
    </CenterView>
    );
};

export default customText;
