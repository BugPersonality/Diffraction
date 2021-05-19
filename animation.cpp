#include<iostream>
#include <SFML/Audio.hpp>
#include <SFML/Graphics.hpp>
#include<math.h>
#include <fstream>
#include <stdio.h>
#include <stdlib.h>
#include<vector>

using namespace std;
using namespace sf;

// double getDistanceBetweenTwoPoints(Point point1, Point point2){
//     return sqrt(pow(point1.x - point2.x, 2) + pow(point1.y - point2.y, 2));
// }

class Back_Groung {
    public:
    Texture texture;
    Sprite sprite;

    Back_Groung(String F)
    {
        texture.loadFromFile(F);
        Vector2u size = texture.getSize();
        sprite.setTexture(texture);
        sprite.setPosition(400, 400);
        sprite.setOrigin(size.x / 2, size.y / 2);
    }
};

class Receiver {
    public:

    float x, y, w, h;

    String file;
    Image image;
    Texture texture;
    Sprite sprite;

    Receiver(String F, float X, float Y, float W, float H)
	{
        file = F;
        w = W; h = H;
        x = X;
        y = Y;

        image.loadFromFile(file);

        image.createMaskFromColor(Color(0, 0, 0));
        texture.loadFromImage(image);
        sprite.setTexture(texture);

        sprite.setPosition(x, y);
        sprite.setOrigin(w / 2, h / 2);
	}

    FloatRect getRect() 
    {
        return sprite.getGlobalBounds();
    }
};

class Hole {
    public:
    Texture texture;
    Sprite sprite;

    Hole(String F)
    {
        texture.loadFromFile(F);
        Vector2u size = texture.getSize();
        sprite.setTexture(texture);
        sprite.setPosition(360, 388);
        sprite.setOrigin(size.x / 2, size.y / 2);
    }

    FloatRect getRect() 
    {
        return sprite.getGlobalBounds();
    }
};

class Electron{
    public:
    
    float x;
    float y;
    float speed;

    float dx, dy;

    CircleShape point;

    Electron() {
        point = CircleShape(5.f);
        point.setFillColor(Color::Green);
        x = 75;
        y = 388;
        speed = 0.1;
        dx = speed;
        dy = 0;
        point.setPosition(x, y);
    }

    void update(float time) {
        x += (dx * time);
        y += dy * time;              
       
        point.setPosition(x, y);
    }

    FloatRect getRect() 
    {
        return point.getGlobalBounds();
    }
};


int main() {
    Clock clock;
    
    RenderWindow window(VideoMode(800, 800), "BrownianMotion");

    vector<Electron> points;
    vector<int> keys; 
    
    for(int i = 0; i < 1; i++) {
        points.push_back(Electron());
    }

    ifstream infile("resources/keys.txt");
    
    int count, countOFKeys;
    infile >> count >> countOFKeys;
    
    for (int i = 0; i < count; ++i) {
        int key;
        infile >> key;
        keys.push_back(key);
    }

    infile.close();

    // for (auto& key : keys)
    //     cout << key << endl;

    Back_Groung background("resources/imgs/labTable.jpg");
    Hole hole("resources/imgs/hole.png");

    while (window.isOpen()) {
        // Events 
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed) {
                window.close();
            }  
        }

        // Calculations
        float time = clock.getElapsedTime().asMicroseconds();
        clock.restart();
        time = time / 800;

        points[0].update(time);

        if (hole.getRect().intersects(points[0].getRect())) {
            points[0].dx = 0;
        }

        // Drawing 
        window.clear();
        window.draw(hole.sprite);
        window.draw(background.sprite);
        window.draw(points[0].point);
        window.display();
    }

    return 0;
}