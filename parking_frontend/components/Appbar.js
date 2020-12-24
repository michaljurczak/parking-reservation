import React from 'react';
import { Appbar } from 'react-native-paper';

import PARKING_APP_CONFIG from './ParkingAppConfig.json';
import SearchDate from './SearchDate';

/**
 * Component for displaying application top bar.
 * @param {string} setDate Date in format YYYY-MM-DD
 * @return {Appbar} Returns Appbar component
 */

const PkAppbar = props => (
  <Appbar.Header>
    <Appbar.Content title={PARKING_APP_CONFIG.appTitle} />
    <SearchDate setDate={props.setDate} />
  </Appbar.Header>
);

export default PkAppbar;
