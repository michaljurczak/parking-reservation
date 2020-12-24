import React from 'react';
import { Appbar, TextInput } from 'react-native-paper';

import PARKING_APP_CONFIG from './ParkingAppConfig.json';

import moment from 'moment';

/**
 * Component (input element with button) for getting available parking spots in a specific day
 * @param {string} placeholder  Placeholder text in the input box
 * @param {string} value Input date string. Accepts all string values.
 * @param {funciton} onChangeText Method reference for handling input changes.
 * @param {function} onPress Method reference for handling clicked magnify icon.
 * @returns {DateSearch} Returns component responsible for getting parking spots in a specific day.
 */

const dateSearch = props => {
  const [inputDate, setInputText] = React.useState(moment().format(PARKING_APP_CONFIG.dateFormat));

  const setFullRequestDate = () => {
    const time = moment().format(PARKING_APP_CONFIG.hourFormat);
    const fullDate = inputDate + "/" + time + "/";
    props.setDate(fullDate);
  };

  return (
    <>
      <TextInput
        style={{ height: '50%' }}
        placeholder={PARKING_APP_CONFIG.dateFormat}
        value={inputDate}
        onChangeText={setInputText} />
      <Appbar.Action icon="magnify" onPress={setFullRequestDate} color={'white'} />
    </>
  );
};

export default dateSearch;
