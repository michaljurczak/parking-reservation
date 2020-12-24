import React from 'react';
import { configure, shallow } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

configure({adapter: new Adapter()});

import ParkingSpot from '../components/ParkingSpots/ParkingSpot';

import StyledTitle from '../components/styled/StyledTitle';

describe('<ParkingSpot />', () => {
  let wrapper;

  const props = {
    place_number: "1",
    reservations: []
  }

  beforeEach(() => {
    wrapper = shallow(<ParkingSpot content={props}/>);
  });

  it('should render 1 StyledTitle with text 1', () => {
    expect(wrapper.find(StyledTitle)).toHaveLength(1);
    expect(wrapper.contains(<StyledTitle>1</StyledTitle>)).toEqual(true);
  });

  it('should render 1 ParkingSpot with no text', () => {
    wrapper.setProps({
      content: {
        ...props,
        place_number: null
      }
    });
    expect(wrapper.find(StyledTitle)).toHaveLength(1);
    expect(wrapper.contains(<StyledTitle></StyledTitle>)).toBe(true);
  });
});
