# What is this about?

The purpose of the project is to build a robot car that could learn by itself driven by curiousity.

The main inspiration for this is: https://pathak22.github.io/noreward-rl/

## Hardware:

### Chassis, Wheels and Motors

I first printed (3D Printed rig)[https://www.thingiverse.com/thing:2450012] but it did not work very well. I am going for a laser cut chassis. I think I will eventually go for the Mecanum wheels.


For now, I am going for a normal wheels and motors not powerful ones something like this: https://www.aliexpress.com/item/4001089097866.html?spm=a2g0o.cart.0.0.4dab3c00VMj2Yr&mp=1


### Processor

I am going ahead with raspberry pi with 1GB RAM. The reason to go with that is because we need to run neural network model on this therefore we need highend processor. Probably, we would go for Nvidia Nano afterwards.

### Sensors

My plan is to have:

+ A camera with pan-tilt motors
+ Wifi Connection
+ Ultrasonic sensors

## Software and design

### First Design

On big The Q-Learning based model with Tensorflow. 

The Ultrasonic sensor will consider it a collision if something is closer than 3cms. It won't let the motors moves if something is closer than 3cms.

The reward will be how many meters it walked per minutes and failure will be if it collided with something.

The raspberry pi will keep taking pictures, action it took and whether it caused any collision. It will store the images as file and append to csv file the action it took and the collision caused along with timestamp.

Raspberry pi will also monitor if a new model is available to download. If it is it will load the new model and unload the previous model.

Pi will take a picture, feed it to model and take the step as suggested by model. Then it will save the result along with action it took and the name of the picture.

Periodically, a service on the GPU server will try to rsync the files to a GPU machine's folder. It will also delete the files.

The new files will be considered in the training for the next phase.

## Second Design

It will be based on the Curiosity Based Learner.
