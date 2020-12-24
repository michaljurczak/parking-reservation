import React, { useState, useEffect } from 'react';

import axios from 'axios';
import moment from 'moment';

import { API_URL } from '@env'

import { Provider as PaperProvider } from 'react-native-paper'

import PARKING_APP_CONFIG from './ParkingAppConfig.json';

import Container from './styled/Container';
import ParkingAppbar from './Appbar';
import ParkingSpots from './ParkingSpots/ParkingSpots';
import PkSnackbar from './Snackbar';

import Loading from './Loading';

import Context from './Context';

axios.defaults.baseURL = API_URL;

/**
 * Component for displaying initial app view.
 * @returns {ParkingApp} Returns component with initial app view.
 */

const ParkingApp = () => {
  const [getAvailableParkingSpots, setAvailableParkingSpots] = useState([]);
  const [getCurrentDateAndTime, setCurrentDateAndTime] = useState(moment().format(PARKING_APP_CONFIG.dateTimeFormat));
  const [isDataLoading, setLoadingDataStatus] = useState(true);
  const [reloadView, setReloadView] = useState(false);

  const [responseMessage, setResponseMessage] = useState(null);
  const [isSnackbarVisible, setSnackbarVisible] = useState(false);

  const toggleSnackbar = () => {
    setSnackbarVisible(true);
    setSnackbarVisible(false);
  };

  const setMessageAndShowHandler = message => {
    setResponseMessage(message);
    toggleSnackbar();
  };

  useEffect(() => {
    let isMounted = true;
    setLoadingDataStatus(true);

    axios.get('/' + getCurrentDateAndTime)
      .then(res => {
        if (!isMounted) {
          return;
        }
        setLoadingDataStatus(false);
        setAvailableParkingSpots(res.data);
        setReloadView(false);
      }).catch(err => {
        setMessageAndShowHandler(err.message);
      });
    return () => { isMounted = false };
  }, [getCurrentDateAndTime, reloadView]);

  let mainScreenComponent = <Loading animating={isDataLoading} />;

  if (!isDataLoading) {
    mainScreenComponent =
      <ParkingSpots
        availableParkingSpots={getAvailableParkingSpots}
        numColumns={PARKING_APP_CONFIG.numColumns}
        currentDateTime={getCurrentDateAndTime}
        reloadView={setReloadView}
        setMessageAndShowSnackbar={setMessageAndShowHandler}
      />;
  }

  const mainView = (
    <>
      {mainScreenComponent}
      <PkSnackbar
        visible={isSnackbarVisible}
        text={responseMessage}
        seconds={PARKING_APP_CONFIG.snackbarDisplaySeconds}
      />
    </>
  );

  return (
    <PaperProvider>
      <Context.Provider value={{ user: { id: 1, company: 2 } }}>
        <Container>
          <ParkingAppbar setDate={setCurrentDateAndTime} />
          {mainView}
        </Container>
      </Context.Provider>
    </PaperProvider>
  );
};

export default ParkingApp;
