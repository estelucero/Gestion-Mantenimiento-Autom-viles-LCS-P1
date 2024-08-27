import React from "react";
import styled from "styled-components";

import LogoImg from "../../images/logos/logo.png";

const BrandLogoContainer = styled.div`
  display: flex;
  align-items: center;
`;

const LogoImage = styled.div`
   width: ${({ size }) => (size ? size + "px" : "4em")};
  height: ${({ size }) => (size ? size + "px" : "3em")};

  img {
    width: 100%;
    height: 100%;
  }
`;

const LogoTitle = styled.h2`
  margin: 0;
  font-size: ${({ size }) => (size ? size + "px" : "20px")};
  color: ${({ color }) => (color ? color : "#fff")};
  font-weight: 900;
  margin-left: 6px;
`;

export function BrandLogo(props) {
const { logoSize, textSize, color, hideLogo } = props;

    return <BrandLogoContainer>
    <LogoImage size={logoSize}>
        <img src={LogoImg} alt="ControlCar logo"/>
    </LogoImage>
    <LogoTitle size={textSize}>ControlCar</LogoTitle>
    </BrandLogoContainer>
}