#include <iostream>
#include <vector>
#include <ctime>

struct tradeRes 
{
    std::string type;
    std::time_t time;
    float price;
};

struct infoMarket
{
    std::vector <float> prices;
    std::vector <float> middlePrices;
    std::vector <float> upBBs;
    std::vector <float> downBBs;
    std::vector <std::time_t> times;
};

std::vector<tradeRes> trade(const infoMarket& data) {
    std::vector <tradeRes> trades;
    bool isOpen = false;
    std::string isType;
    float isClosePrice = 0.0;

    for (int i = 0; i < data.prices.size(); i++)
    {
        if (isOpen == false)
        {
            if (data.prices[i] >= data.upBBs[i])
            {
                trades.push_back({ "sell", data.times[i], data.prices[i] });
                isOpen = true;
                isType = "sell";
                isClosePrice = data.prices[i];
            }
            else if (data.prices[i] <= data.downBBs[i])
            {
                trades.push_back({ "buy", data.times[i], data.prices[i] });
                isOpen = true;
                isType = "buy";
                isClosePrice = data.prices[i];
            }
        }
        else 
        {
            if ( isType == "sell" && data.middlePrices[i] >= data.prices[i])
            {
                trades.push_back({ "buy", data.times[i], data.prices[i] });
                isType = "clear";
                isOpen = false;
            }
            else if (isType == "buy" && data.middlePrices[i] <= data.prices[i])
            {
                trades.push_back({ "sell", data.times[i], data.prices[i] });
                isType = "clear";
                isOpen = false;
            }
        }
    }
    return trades;
}


int main()
{
    infoMarket data = {
         //Вводим нужные нам данные
    };

    std::vector<tradeRes> trades = trade(data);
    for ( const tradeRes& trade : trades)
    {
        std::cout << "Trade: " << trade.type << " at time " << trade.time << " with price " << trade.price << std::endl;
    }
}