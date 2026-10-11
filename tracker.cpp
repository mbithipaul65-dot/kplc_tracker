#include <iostream>
#include <string>
#include <cmath>
#include <iomanip>
#include <sstream>
#include <stdexcept>

int main(int argc, char* argv[]) {
    // Validate argument count strictly
    if (argc < 5) {
        std::cerr << "{\"error\":\"Invalid argument count\"}" << std::endl;
        return 1;
    }

    std::string meter_number = argv[1];
    std::string buyer_phone = argv[2];
    double balance = 0.0;
    double daily_usage = 0.0;

    // Secure numerical conversion handling
    try {
        balance = std::stod(argv[3]);
        daily_usage = std::stod(argv[4]);
    } catch (const std::exception& e) {
        std::cerr << "{\"error\":\"Invalid numerical input\"}" << std::endl;
        return 1;
    }

    double hourly_usage = daily_usage / 24.0;
    double new_balance = std::max(0.0, balance - hourly_usage);

    // Personalized threshold (2-day buffer)
    double personalized_threshold = daily_usage * 2.0;

    double hours_left = (hourly_usage > 0) ? (new_balance / hourly_usage) : 0;
    int days = static_cast<int>(hours_left / 24);
    int rem_hours = static_cast<int>(hours_left) % 24;

    std::ostringstream timeStream;
    if (days > 0) {
        timeStream << days << " days " << rem_hours << " hours";
    } else {
        timeStream << rem_hours << " hours";
    }

    bool needs_alert = (new_balance > 0.0 && new_balance <= personalized_threshold);

    // JSON response output
    std::cout << "{"
              << "\"meter_number\":\"" << meter_number << "\","
              << "\"buyer_phone\":\"" << buyer_phone << "\","
              << "\"new_balance\":" << std::fixed << std::setprecision(2) << new_balance << ","
              << "\"time_left\":\"" << timeStream.str() << "\","
              << "\"needs_alert\":" << (needs_alert ? "true" : "false")
              << "}" << std::endl;

    return 0;
}