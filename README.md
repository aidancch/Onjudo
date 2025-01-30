# Onjūdō: Your AI Real Estate Agent

![Onjudo Header Logo](https://github.com/aidancch/Onjudo/blob/main/onjudo_header_logo.png)

## Overview

Onjūdō is a website that helps people easily find their dream homes. Users can skip managing filters and search boxes by talking to our virtual real estate agent. All they have to do is specify what they are looking for in a house, and Onjūdō will find it for them. Currently, Onjūdō can handle location, size, price, the number of beds, and the number of baths. Onjūdō is also able to give recommendations for where to look for houses when asked for them.

## Contributors

- [Aidan Chiu](mailto:aidanchiuch@gmail.com)
- [Thomas Lavery](mailto:thomas.lavery18@gmail.com)

## Table of Contents

- [Onjūdō](#onjūdō)
  - [Overview](#overview)
  - [Contributors](#contributors)
  - [Table of Contents](#table-of-contents)
  - [Inspiration](#inspiration)
  - [Goals](#goals)
  - [Built With](#built-with)
  - [Challenges](#challenges)
  - [Accomplishments](#accomplishments)
  - [What We Learned](#what-we-learned)
  - [What's Next](#whats-next)
  - [How to run](#how-to-run)

## Inspiration

Searching for homes online by navigating sites like Zillow can become very tedious and challenging for the elderly or vision impaired. The goal of this project is to create an experience that is the same as talking to a real estate agent while receiving listings in real-time based on user preferences. The name, "Onjūdō," means peaceful home in Japanese.

## Goals

- Provide real estate search features that aren't offered anywhere else.
- Create a site that is accessible and convenient for anyone who's looking for their dream house.

## Built With

- Frontend
    - React
    - TailwindCSS
    - Shadcn
    - TypeScript
- Backend
    - Python
    - Flask
    - SocketIO

## Challenges

1. Since we wanted real-time chat, reducing latency was a top priority in order to give a good user experience. Because our website is passing and processing vast amounts of data per second, it can become very slow and cumbersome. This is why we spent a lot of time and effort ensuring things were connected effectively, which made our program speed up. 
3. Another challenge was getting the LLMs to do what we wanted. Since LLMs can do and return slightly different things based on user input, many insidious bugs would arise because our code wasn't robust enough to handle garbage input. As a result, the garbage output would crash everything. To fix this, instead of spending hours testing various conditions, we forced properly formatted responses through better prompt engineering.

## Accomplishments

1. As first years in our first hackathon, we didn't think we would get as far as we did.
2. Without much experience with front-end development, we are proud to be able to pull off the clean and readable interface with integration of many features like Google Maps API.

## What We Learned

- Everything we did in this project was new to us. We learned how LLMs worked behind the scenes, how to use their APIs, and how to use system prompts to control how LLMs responded. We also figured out how to use React, Tailwind, and CSS to integrate many features and make an easily navigable site with a lot of interaction.

## What's Next

- One of our goals is to provide unique real estate search features. To this end, we want to add a toggleable map for crime and air quality so that users can also search for houses by those metrics.
- We believe everyone should be able to use our website, so we want to increase accessibility by adding text-to-speech responses for the LLM response and speech-to-text input for users.
- Finally, we want to add accounts and bookmark features so users can come back and see houses they found earlier

## How to run

```
cd my-app/
npm run dev
python3 backend/app.py
```

We apologize for not utilizing containers like Docker to build the project with. We had limited time during our hackathon and proceeded without doing so (which we regretted as we had several compatability issues across devices). If you like this project and want to collaborate, please reach out to us! We would love Docker support, and a proper ```requirements.txt``` file.
