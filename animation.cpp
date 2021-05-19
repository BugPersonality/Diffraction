#include <iostream>
#include <SFML/Audio.hpp>
#include <SFML/Graphics.hpp>
#include <algorithm>
#include <cmath>
#include <fstream>
#include <stdio.h>
#include <stdlib.h>
#include <vector>

using namespace std;
using namespace sf;

double getDistanceBetweenTwoPoints(Vector2f point1, Vector2f point2){
     return sqrt(pow(point1.x - point2.x, 2) + pow(point1.y - point2.y, 2));
}

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

    Receiver(int count) {
        font.loadFromFile("resources/calibri.ttf");

        for (int i = 0, offset = 0; i < count; i++) {
            RectangleShape rect;

            rect.setSize(Vector2f(70, 350.0/count - 4));
            rect.setPosition(600, 60 + offset);
            rect.setFillColor(Color::Black);
            rect.setOutlineThickness(1);
            

            Text text;
            text.setFont(font);
            text.setString(to_string(count - i));
            text.setPosition(675, 60 + offset + (350.0/count - 4)/2.0 - 15);
            text.setCharacterSize(15);
            text.setStyle(Text::Bold);
            text.setColor(Color::Black);
            
            offset += 350.0/count;

            pair<RectangleShape, pair<Text, int>> toAdd;

            toAdd.first = rect;
            toAdd.second.first = text;
            toAdd.second.second = 0;

            recive.push_back(toAdd);
        }   
	}

    void hit(int index) {
        index = recive.size() - index;

        recive[index].second.second++;
        max_count = max(max_count, recive[index].second.second);

        recive[index].first.setFillColor(Color(rand()%255, rand()%255, rand()%255));

        //recive[index].first.setFillColor(Color(recive[index].second.second/(float)max_count * 255.0, 0, 0, 255));
    }

    Vector2f getPos(int index) {
        index = recive.size() - index;
        return {recive[index].first.getGlobalBounds().left, 
                recive[index].first.getGlobalBounds().top + recive[index].first.getGlobalBounds().height / 2.0}; 
    }

    void draw(RenderWindow& window) {
        for (auto& rec : recive) {
            window.draw(rec.first);
            window.draw(rec.second.first);
        }
    }
private:
    int max_count;
    Font font;
    vector<pair<RectangleShape, pair<Text, int>>> recive;
};

class Electron{
    public:
    
    float x;
    float y;
    float speed;

    float dx, dy;

    CircleShape point;

    Electron() 
        : flag_hole(false)
    {
        point = CircleShape(5.f);
        point.setFillColor(Color::Red);
        x = 75;
        y = 388;
        speed = 0.1;
        dx = speed;
        dy = 0;
        point.setPosition(x, y);
    }

    bool getColl() 
    {
        return flag_hole;
    }

    void move(float time) {
        x += (dx * time);
        y += dy * time;

        if (flag_hole)
        {
            point.setPosition(Vector2f(cosX*x + 360, -sinY*x + 390));
        }
        else
        {
            point.setPosition(x, y);
        }
    }

    int getIndexRec() {
        return indexRec;
    }

    void hitHole(Vector2f pos, int index) {
        indexRec = index;
        posRecive = pos;
        flag_hole = true;
        // {360, 390}
        cosX = (pos.x - 360)/getDistanceBetweenTwoPoints({360, 390}, pos);
        sinY = (390 - pos.y)/getDistanceBetweenTwoPoints({360, 390}, pos);
        x = 0;
        y = 0;
    }

    void draw(RenderWindow& window) {
        window.draw(point);
    }

    FloatRect getRect() 
    {
        return point.getGlobalBounds();
    }
private:
    double cosX, sinY;
    int indexRec;
    bool flag_hole;
    Vector2f posRecive;
};


int main() {
    Clock clock, clockAdd;
    
    RenderWindow window(VideoMode(800, 800), "BrownianMotion");
    RectangleShape hole;

    hole.setFillColor(Color::Transparent);
    hole.setPosition(360, 365);
    hole.setSize(Vector2f(10, 50));

    vector<Electron> points;
    vector<int> keys; 

    ifstream infile("resources/keys.txt");
    
    int count, countOFKeys;
    infile >> count >> countOFKeys;
    
    for (int i = 0; i < count; ++i) {
        int key;
        infile >> key;
        keys.push_back(key);
    }

    infile.close();

    Back_Groung background("resources/imgs/labTable.jpg");

    Receiver reciev(countOFKeys);

    int index_key = 0, count_point = 0;
    float old_time = 0, offset_time = 10;

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

        if (count_point < keys.size() && old_time < clockAdd.getElapsedTime().asMilliseconds())
        {
            points.emplace_back(Electron());
            old_time += offset_time;
            count_point++;
        }

        time = time / 800;
        
        for (auto it = points.begin(); it != points.end(); it++)
        {
            it->move(time);

            if (!it->getColl() && index_key < keys.size() && hole.getGlobalBounds().intersects(it->getRect())) 
            {
                it->hitHole(reciev.getPos(keys[index_key]), keys[index_key]);
                index_key++;
            }

            if (it->getRect().left > 600) {
                reciev.hit(it->getIndexRec());
                it = points.erase(it);
                if (it == points.end())
                    break;
            }    
        }

        // Drawing
        window.clear();
        window.draw(background.sprite);
        window.draw(hole);
        reciev.draw(window);

        for (auto& point : points)
            point.draw(window);
        window.display();
    }

    return 0;
}