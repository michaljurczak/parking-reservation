import React, {useContext} from 'react';

import { Card } from 'react-native-paper';

import StyledParkingSpot from '../styled/StyledParkingSpot';
import StyledTitle from '../styled/StyledTitle';
import StyledParagraph from '../styled/StyledParagraph';
import APP_STYLES from "../styled/AppStyles.json";

import Context from '../Context';

/**
 * Component for displaying parking spot as a card.
 * @param {function} onPress Handler for a function when onPress
 * @param {number} content Parking spot number
 * @return {ParkingSpot} Returns styled parking spot card
 */

const ParkingSpot = props => {
  const reservations = props.content.reservations;
  const place_number = props.content.place_number;
  const {company} = props.content;

  const context = useContext(Context);
  let canChange = true;
  let removeReservation = false;
  let reservationId = null;

  const pressHandler = () => {
    context.setParkingSpot(place_number);
    if (!canChange) {
      return;
    }

    if(removeReservation) {
      context.setRemoveReservation(true);
      context.setParkingId(reservationId);
    }
    context.press();
  }


  let companyName = '';
  let bgColor = APP_STYLES.appBackground;
  
  const disableReservation = () => {
    bgColor = APP_STYLES.reservedBackground;
    canChange = false;
  }
  
  if (company) {
    companyName = company.name;
    if (company.id !== context.user.company) {
      disableReservation();
    }
  }

  if (reservations.length) {
    reservations.map((reservation) =>{
      if (reservation.user === context.user.id) {
        bgColor = APP_STYLES.canRemoveReservationBackground;
        removeReservation = true;
        reservationId = reservation.id;
        return;
      }
      disableReservation();
    });
  }

  return (
    <StyledParkingSpot onPress={pressHandler} bgColor={bgColor}>
      <Card.Content>
        <StyledTitle>{place_number}</StyledTitle>
        <StyledParagraph>{companyName}</StyledParagraph>
      </Card.Content>
    </StyledParkingSpot>
  );
};

export default ParkingSpot;