import styled from 'styled-components/native';
import { Card } from 'react-native-paper';

/**
 * Component for displaying Parking Spot card.
 * @return {Card} Returns styled Card
 */

const StyledParkingSpot = styled(Card)`
    flex: 1;
    margin: 3px;
    background-color: ${props => props.bgColor};
}`;

export default StyledParkingSpot;
