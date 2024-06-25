#include <windows.h>
#include <opencv2/opencv.hpp>
#include <iostream>

// Function to capture a screenshot of a specified region
cv::Mat captureScreen(const RECT& region) {
    int width = region.right - region.left;
    int height = region.bottom - region.top;

    HDC hScreen = GetDC(NULL);
    HDC hDC = CreateCompatibleDC(hScreen);
    HBITMAP hBitmap = CreateCompatibleBitmap(hScreen, width, height);
    SelectObject(hDC, hBitmap);

    BitBlt(hDC, 0, 0, width, height, hScreen, region.left, region.top, SRCCOPY);
    BITMAPINFOHEADER bi = { sizeof(BITMAPINFOHEADER), width, -height, 1, 32, BI_RGB, 0, 0, 0, 0, 0 };
    cv::Mat mat(height, width, CV_8UC4);
    GetDIBits(hDC, hBitmap, 0, height, mat.data, (BITMAPINFO*)&bi, DIB_RGB_COLORS);

    DeleteObject(hBitmap);
    DeleteDC(hDC);
    ReleaseDC(NULL, hScreen);

    return mat;
}

// Function to move the mouse to a specified position
void moveMouse(int x, int y) {
    SetCursorPos(x, y);
}

// Function to find the ball's x position (assumes ball is red)
int findBallX(const cv::Mat& img) {
    cv::Mat hsv, mask;
    cv::cvtColor(img, hsv, cv::COLOR_BGR2HSV);

    // Define range for red color and apply mask
    cv::Scalar lowerRed = cv::Scalar(0, 120, 70);
    cv::Scalar upperRed = cv::Scalar(10, 255, 255);
    cv::inRange(hsv, lowerRed, upperRed, mask);

    cv::Moments m = cv::moments(mask, true);
    if (m.m00 > 0) {
        return int(m.m10 / m.m00);
    }
    return -1;
}

// Function to toggle the running state
bool toggleRunning() {
    static bool running = false;
    running = !running;
    return running;
}

int main() {
    RECT region = { 0, 0, 800, 600 };  // Define the capture region
    std::cout << "Press 'T' to start/stop the program." << std::endl;

    while (true) {
        if (GetAsyncKeyState('T') & 0x8000) {
            bool running = toggleRunning();
            std::cout << (running ? "Program started" : "Program stopped") << std::endl;
            Sleep(300);  // Debounce the key press
        }

        static bool running = false;
        if (running) {
            cv::Mat img = captureScreen(region);
            int ballX = findBallX(img);
            if (ballX != -1) {
                moveMouse(ballX + region.left, region.bottom - 50);  // Adjust for region offset
            }
        }

        Sleep(10);  // Control the speed
    }

    return 0;
}