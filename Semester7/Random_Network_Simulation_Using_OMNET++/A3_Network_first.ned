simple Node
{
    parameters:
        @display("i=block/routing");
    gates:
        inout port[];  // declare two way connections
}


network A3_Network_first
{
    //we can customize the channel based on our requirements
    types:
        channel Channel extends ned.DelayChannel {
            delay = 100ms;
        }
    submodules:
        Nodes[8]: Node;
    //creating a random network connection
    connections:           
        Nodes[0].port++ <--> Channel <--> Nodes[1].port++;
        Nodes[0].port++ <--> Channel <--> Nodes[2].port++;
        Nodes[1].port++ <--> Channel <--> Nodes[3].port++;
        Nodes[1].port++ <--> Channel <--> Nodes[4].port++;
        Nodes[1].port++ <--> Channel <--> Nodes[7].port++;
        Nodes[3].port++ <--> Channel <--> Nodes[7].port++;
        Nodes[4].port++ <--> Channel <--> Nodes[7].port++;
        Nodes[2].port++ <--> Channel <--> Nodes[7].port++;
        Nodes[2].port++ <--> Channel <--> Nodes[5].port++;
        Nodes[2].port++ <--> Channel <--> Nodes[6].port++;
        Nodes[5].port++ <--> Channel <--> Nodes[7].port++;
        Nodes[6].port++ <--> Channel <--> Nodes[7].port++;
}
