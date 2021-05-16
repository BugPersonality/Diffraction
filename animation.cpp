#include<iostream>
#include <SFML/Audio.hpp>
#include <SFML/Graphics.hpp>
#include<math.h>
#include <fstream>
#include <stdio.h>
#include <stdlib.h>

using namespace std;
int main(){
    int w = 700; int h = 700;
    int n = 70;
    srand (time(NULL));
    sf::RenderWindow window(sf::VideoMode(w, h), "Diffraction");    
    while (window.isOpen())
    {        
        sf::Event event;
        while (window.pollEvent(event))
        {
            if (event.type == sf::Event::Closed)
                window.close();
        }

        window.clear();
        window.display();
    }

    return 0;
}