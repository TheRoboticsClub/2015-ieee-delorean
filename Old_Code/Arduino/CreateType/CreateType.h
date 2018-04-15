#include <Arduino.h>;

class CreateType{
	public:
		struct Order{
	   		String Move = "";
	   		int Value= 0;
 		};
 		
		Order AddMyType(String MyStr);

	private:
		String _MyStr;
		Order _MyOrder;

};
