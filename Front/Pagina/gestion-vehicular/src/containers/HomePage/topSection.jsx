import React from "react";
import styled from "styled-components";
import { BrandLogo } from "../../components/brandLogo";
import { Marginer } from "../../components/marginer";

import TopSectionBackgroundImg from "../../images/imagenes/fondo-principal.jpg";


const TopSectionContainer = styled.div`
  width: 100%;
  height: 800px;
  background: url(${TopSectionBackgroundImg}) no-repeat;
  background-position: 0px 60px;
  background-size: cover;
`;

const BackgroundFilter = styled.div`
  width: 100%;
  height: 100%;
  background-color: rgba(38, 70, 83, 0.7);
  display: flex;
  flex-direction: column;
`;

const TopSectionInnerContainer = styled.div`
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-evenly;
`;

const StandoutImage = styled.div`
  width: 44em;
  height: 34em;

  img {
    width: 100%;
    height: 100%;
  }
`;

const LogoContainer = styled.div`
  display: flex;
  align-items: flex-start;
  flex-direction: column;
`;

const SloganText = styled.h3`
  margin: 0;
  line-height: 1.4;
  color: #fff;
  font-weight: 500;
  font-size: 40px;
`;

export function TopSection(props) {
    const { children } = props;

    return (
    <TopSectionContainer>
        <BackgroundFilter>
            {children}
            <TopSectionInnerContainer>
                <LogoContainer>
                    <BrandLogo logoSize={80} textSize={55}/>
                    <Marginer direction="vertical" margin={10}/>
                    <SloganText>Gestionar vehiculos</SloganText>
                    <Marginer direction="vertical" margin={15}/>
                </LogoContainer>
                <StandoutImage>

                </StandoutImage>
            </TopSectionInnerContainer>
        </BackgroundFilter>
        </TopSectionContainer>
    );
}