# ChowHound

Our project for SDS Labs' annual hackathon 2018 

Food wastage plagues the average Bhawan mess at IITR. This project is an effort to combat this. Hopefully, our solution or a variation thereof can help deliver delicious food is exciting combinations to students thus minimizing wastage. 

Our project uses a neural network in a reinforcement learning setup. It receives all the possible food items as input and the output is a prediction for the next meal and an estimate of the wastage. Initially, we force the network to learn the correlation between different meals and the measured wastage (In % weight) by forcing inputs according to what was cooked in the mess. Subsequently, the network starts making better predictions and we allow the network to control the kitchen. 

The mess is simulated as in artificial environment which assumes the food wastage as some function of how popular a particular item is. The neural net learns using policy gradients and seems to converge on the wastage function quite quickly. 

For the future prospects of this project, we want to deploy this application as a web app with visualizations.  