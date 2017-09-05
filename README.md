# Arduino-Pi-Irrigation
Weather-concious automated watering system built using a network of microcontrollers and local forecast data.

View the slides for my recent presentation [here](https://docs.google.com/presentation/d/e/2PACX-1vRUcPLF_Tc3twKdrdGbYBv-fllPakoCYKyDjmxIf2WdxU_leEsZdf-I8NOx8RZEK6N9C75NVcK9myaj/pub?start=false&loop=false&delayms=3000 "Intelligent Irrigation presentation")

# Data flow diagram
![Built using draw.io](https://lh4.googleusercontent.com/2GCr2gln68PA1_tPKZICo4TYQQBdutg00TPXRqKv_i6U4tDBrhABkgeMhZUKr0pyjgmHfvnkaULOTvM=w1366-h654)

A high-level data flow diagram denoting the process involved in the system.

# Currently in development
* Integration of 2.4Ghz transcievers for long range communication
* Formation of data packets
* Call/response functionality to act as a health check between microcontrollers before requesting data
* Processing of data packets into CSV's for further processing
