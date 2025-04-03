#include <stdio.h>
#include <string.h>
#include <omnetpp.h>
#include "a3firstmsg_m.h"

using namespace omnetpp;

class Node : public cSimpleModule
{
  private:
    long numSent;
    long numReceived;
    cHistogram hopCountStats;
    cOutVector hopCountVector;

  protected:
    virtual A3_First_MSG *generateMessage();
    virtual void forwardMessage(A3_First_MSG *msg);
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;

    // The finish() function is called by OMNeT++ at the end of the simulation:
    virtual void finish() override;
};

Define_Module(Node);

void Node::initialize()
{
    // Initialize variables
    numSent = 0;
    numReceived = 0;
    WATCH(numSent);
    WATCH(numReceived);

    hopCountStats.setName("hopCountStats");
    hopCountVector.setName("HopCount");

    // Module 0 sends the first message
    if (getIndex() == 0) {
        // Add static text to the canvas
        cTextFigure *text = new cTextFigure("StaticText");
       // The text to display
        text->setText("\"Wireless Communication \n \t Systems\" ");
        text->setPosition(cFigure::Point(0,400));     // Position on the canvas
        text->setColor(cFigure::BLUE);                   // Text color
        text->setFont(cFigure::Font("Arial", 20));       // Font style and size
        getParentModule()->getCanvas()->addFigure(text);

        // Boot the process scheduling the initial message as a self-message.
        A3_First_MSG *msg = generateMessage();
        scheduleAt(0.0, msg);
    }
}

void Node::handleMessage(cMessage *msg)
{
    A3_First_MSG *ttmsg = check_and_cast<A3_First_MSG *>(msg);

    if (ttmsg->getDestination() == getIndex()) {
        // Message arrived
        int hopcount = ttmsg->getHopCount();
        EV << "Message " << ttmsg << " arrived after " << hopcount << " hops.\n";
        bubble("ARRIVED, starting new one!");

        // update statistics.
        numReceived++;
        hopCountVector.record(hopcount);
        hopCountStats.collect(hopcount);

        delete ttmsg;

        // Generate another one.
        EV << "Generating another message: ";
        A3_First_MSG *newmsg = generateMessage();
        EV << newmsg << endl;
        forwardMessage(newmsg);
        numSent++;
    }
    else {
        // We need to forward the message.
        forwardMessage(ttmsg);
    }
}

A3_First_MSG *Node::generateMessage()
{
    // Produce source and destination addresses.
    int src = getIndex();
    int n = getVectorSize();
    int dest = intuniform(0, n-2);
    if (dest >= src)
        dest++;

    char msgname[20];
    sprintf(msgname, "From Source %d to Destination %d", src, dest);

    // Create message object and set source and destination field.
    A3_First_MSG *msg = new A3_First_MSG(msgname);
    msg->setSource(src);
    msg->setDestination(dest);
    return msg;
}

void Node::forwardMessage(A3_First_MSG *msg)
{
    // Increment hop count.
    msg->setHopCount(msg->getHopCount()+1);

    // Same routing as before: random gate.
    int n = gateSize("port");
    int k = intuniform(0, n-1);

    EV << "Forwarding message " << msg << " on port[" << k << "]\n";
    send(msg, "port$o", k);
}

void Node::finish()
{
    // This function is called by OMNeT++ at the end of the simulation.
    EV << "Sent:     " << numSent << endl;
    EV << "Received: " << numReceived << endl;
    EV << "Hop count, max:    " << hopCountStats.getMax() << endl;

    recordScalar("#sent", numSent);
    recordScalar("#received", numReceived);

    hopCountStats.recordAs("hop count");
}
