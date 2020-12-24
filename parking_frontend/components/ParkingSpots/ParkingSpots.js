import React, { useContext } from 'react';

import { FlatList } from 'react-native';

import PARKING_APP_CONFIG from '../ParkingAppConfig.json';

import Context from '../Context';
import CustomText from '../styled/CustomText';
import ParkingSpot from './ParkingSpot';
import ParkingDialog from '../Dialog';

import axios from 'axios';

const headers = {
  "Authorization": "Basic YWRtaW46YWRtaW4=",    //DEMO purposes - jwt will be used. user admin password admin in the database
  "Content-Type": "application/json"
}

/**
 * Component for displaying parking spots as a list.
 * @param {Array} availableParkingSpots Array with JSON objects in format {"place_number" : 1, "company": "Company A"}.
 * @param {number} numColumns Number of rows displayed in an app.
 * @param {function} setMessageAndShowSnackbar Function handler for setting text and toggling Snackbar visibility status
 * @return {ParkingSpots} Returns styled parking spots Flat List
 */

const ParkingSpots = props => {
  const context = useContext(Context);
  let availableParkingSpotsLength = props.availableParkingSpots.length;

  const [isVisible, setVisibility] = React.useState(false);
  const [parkingSpot, setParkingSpot] = React.useState(null);
  const [removeReservation, setRemoveReservation] = React.useState(false);
  const [parkingId, setParkingId] = React.useState(null);

  const showModal = () => setVisibility(true);
  const hideModal = () => {
    setVisibility(false);
    setRemoveReservation(false);
    setParkingId(null);
  };

  const contextValues = {
    setParkingSpot: setParkingSpot,
    user: context.user,
    press: showModal,
    setRemoveReservation: setRemoveReservation,
    setParkingId: setParkingId,
  };

  const parseDate = dateStr => dateStr.split('/')[0];  //will be removed when booking
  //parking spots for a certain period of time will be available

  const setMessageAndReloadView = message => {
    props.setMessageAndShowSnackbar(message);
    props.reloadView(true);
  }

  const confirmBookingSpotHandler = () => {
    if (removeReservation) {
      axios.delete("remove-reservation/" + parkingId + "/", {
        headers: headers
      }
      ).then(_ => {
        setMessageAndReloadView(PARKING_APP_CONFIG.successReservation);
      }).catch(_ => {
        setMessageAndReloadView(PARKING_APP_CONFIG.notFoundReservation);
      });
      hideModal();
      return;
    }

    const parsed_date = parseDate(props.currentDateTime);
    axios.post(PARKING_APP_CONFIG.ReserveUri, {
      "reservation_date": parsed_date,
      "parking_spot": parkingSpot
    },
      {
        headers: headers
      }
    ).then(res => {
      const confirmMessage = (PARKING_APP_CONFIG.reservedSpotFor +
        res.data.parking_spot + PARKING_APP_CONFIG.for + res.data.reservation_date);
      setMessageAndReloadView(confirmMessage);
    }).catch(
      (err) => {
        const responseMessage = Object.values(err.response.data)[0];
        props.setMessageAndShowSnackbar(responseMessage);
      });
    hideModal();
  };

  if (availableParkingSpotsLength) {
    let message = PARKING_APP_CONFIG.confirmBookingMessage;
    if (removeReservation) {
      message = PARKING_APP_CONFIG.confirmRemovingMessage;
    }
    message = message + parkingSpot;
    return (
      <Context.Provider value={contextValues}>
        <>
          <ParkingDialog
            show={isVisible}
            hide={hideModal}
            title={parkingSpot}
            message={message}
            confirmBooking={confirmBookingSpotHandler}
          />
          <FlatList data={props.availableParkingSpots}
            renderItem={item => <ParkingSpot content={item.item} />}
            keyExtractor={item => item.place_number}
            numColumns={props.numColumns} />
        </>
      </Context.Provider>
    );
  }
  return <CustomText text={PARKING_APP_CONFIG.noAvailableParkingSpotsMessage} />;
};

export default ParkingSpots;
