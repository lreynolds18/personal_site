class Files ( object ):
	def currency(self):
		return '''
################################################################################
## Class Currency
################################################################################

class Currency( object ):
    
    def __init__( self, amount=0.0, currency_code='USD'):
        """
        Initialize an object of the type Currency
        """

        self.__amount = float(0)
        self.__currency_code = 'USD'
        
        if type(amount) == float or type(amount) == int and type(currency_code) == str and currency_code in ['USD', 'EUR', 'SEK', 'CAD', 'CNY', 'GBP']:
            self.__amount = round(float(amount), 2)
            self.__currency_code = currency_code

    def __repr__( self ):
        """
        Returns a string (the representation of the Currency)
        ( amount, currency )
        """
        return ("( {}, {} )".format(self.__amount, self.__currency_code))

    def __str__( self ):
        """
        Returns a string (the representation of the Currency)
        ( amount, currency )
        """
        return self.__repr__()

    def __add__( self, other ):
        """
        Returns the value of two currencies being added together
        Converts the second currency if they are not the same.
        """
        if type(other) == Currency:
            if self.__currency_code == other.__currency_code:
                return Currency(round(self.__amount + other.__amount, 2), self.__currency_code)
            else:
                # calls convert_to method
                same_currency = other.convert_to(self.__currency_code)
                return Currency(round(same_currency.__amount + self.__amount, 2), self.__currency_code)
        else:
            return Currency(round(self.__amount + other, 2), self.__currency_code)
        

    def __radd__( self, other ):
        """
        Returns the value of the first currency in self, return the value of the number in other
        Calls __add__ with the values switched around.
        """
        return self + other

    def __sub__( self, other ):
        """
        Returns the value of one currency minus another currency
        Converts the second currency if they are not the same.
        """
        if type(other) == Currency:
            if self.__currency_code == other.__currency_code:
                return Currency(round(self.__amount - other.__amount, 2), self.__currency_code)
            else:
                # calls convert_to method
                same_currency = other.convert_to(self.__currency_code)
                return Currency(round(self.__amount - same_currency.__amount, 2), self.__currency_code)
        if type(other) == float or type(other) == int:
            return Currency(round(self.__amount - other, 2), self.__currency_code)
        
    def __rsub__( self, other ):
        """
        Returns the value of the first currency plus a number
        Always uses floats to accounts for both int and float
        """
        return Currency(round(other - self.__amount, 2), self.__currency_code)
    
    def convert_to( self, currency_code ):
        """
        If the currency code isn't one of the five or no code given it passes.
        This fuction finds the conversion rate using google finance.
        Then uses the conversion rate to find the new amount.
        Returns a new object type currency.
        """
        # After 16 it uses scientific notation
        # And logically no one is going to convert that much money into another currency.
        if self.__amount == 0:
            return Currency(0, currency_code)
        if currency_code in ['USD', 'EUR', 'SEK', 'CAD', 'CNY', 'GBP'] and len(str(self.__amount)) <= 16:
            if self.__currency_code == currency_code:
                return Currency(self.__amount, self.__currency_code)

            # Takes website and adds the given variables
            import urllib.request
            website = ["https://www.google.com/finance/converter?a=", "&from=", "&to="]
            site = website[0] + str(self.__amount) + website[1] + self.__currency_code + website[2] + currency_code

            # calls the website
            web_obj = urllib.request.urlopen(str(site))
            results_str = str(web_obj.read())
            web_obj.close()

            # Parses results_str
            info = results_str[results_str.find("div id=currency_converter_result>"):18913]
            info = info.split('>')
            
            converted_amount = info[2][:info[2].find(currency_code)]

            # Makes the convert_amount and the currency_code given into an object, Currency
            Out = Currency(float(converted_amount), currency_code)
            return Out
            

    def __gt__( self, other ):
        """
        If both functions are of the type Currency, then compare the amounts and return correct boolean.
        Changes other to the same currency code as self and compares
        Returns the correct boolean
        """
        
        if type(self) != Currency or type(self) != Currency:
            pass
        else:
            if self.__currency_code == other.__currency_code:
                if self.__amount > other.__amount:
                    return True
                else:
                    return False
            else:
                same_currency = other.convert_to(self.__currency_code)
                if self.__amount > same_currency.__amount:
                    return True
                else:
                    return False
		'''
		
	def functionsc(self):
		return """
/* 
 * File:   functions.cpp
 * Author: Lucas Reynolds
 * Section 2 Project 7
 * March 17, 2014
 */

#include<string>
using std::string;
#include<vector>
using std::vector;
#include<map>
using std::map; using std::pair; using std::make_pair;
#include<iterator>
using std::iterator; using std::ostream_iterator;
#include<cctype>
using std::tolower;
#include<algorithm>
using std::transform; using std::sort; using std::copy;
#include<fstream>
using std::ifstream;
#include<sstream>
using std::ostringstream;

string lower_and_strip(string s) {
    /* Given a string, strips non-alphanumeric chars on both ends, lowercase and return results */
    string target = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890";
    string::size_type pos = s.find_first_of(target); //size_t
    string::size_type length = s.find_last_of(target);
    if(pos != string::npos && length != string::npos) // npos would be all non-alphanumeric & length is redundant
        s = s.substr(pos, length+1-pos);
    else // this strips all the non-alphanumeric chars if thats all it contains.
        s = "";
    transform(s.begin(), s.end(), s.begin(), tolower);
    return s;
}

void read_stopwords(vector<string> &v, string file_name) {
    /* Read the words from file_name and stores them in the vector */
    string word;
    ifstream infile;
    infile.open(file_name);
    if(infile.is_open()) {
        while (infile >> word) {
            v.push_back(word);
        }
    }
}

void read_file(map<string, long> &m, vector<string> &stop_list, string file_name) {
    /* Reads the file called file_name, calls lower_and_strip to each word, adds the word to a map */
    string word;
    ifstream infile;
    infile.open(file_name);
    if(infile.is_open()) {
        while (infile >> word) {
            word = lower_and_strip(word);
            if(find(stop_list.begin(), stop_list.end(), word) == stop_list.end() && word != "")
                m[word]++;
        }
    }
}

bool sort_by_long(pair<string, long> pairone, pair<string, long> pairtwo) {
    /* Returns true if the second value is greater
     * Goes off the string if the longs are the same 
     * Used in the sort function */
    if (pairone.second == pairtwo.second)
        return pairone.first < pairtwo.first;
    return pairone.second < pairtwo.second;
}

string print_map(map<string, long> &m, string order) {
    /* if order is alpha return by alphabetic order
     * else order is count return by frequency order */
    string out;
    ostringstream output;

    if(order == "alpha") {
        vector<string> v;
        v = sorted_words(m);
        copy(v.begin(), v.end(), ostream_iterator<string> (output, ", "));
    }
    else if(order == "count")
        vector<pair<string, long> > v; 
        for (auto it=m.begin(); it!=m.end(); it++) {
            v.push_back(make_pair(it->first, it->second));
        }
        sort(v.begin(), v.end(), sort_by_long);
    for(const auto& value : v)
        output << value.first << "-" << value.second << ", ";
    out = output.str();
    return out.substr(0, -2);
}

vector<string> sorted_words(map<string, long> &m) {
    /* puts words in vector by sorted order */
    // sorted words would do this by itself
    vector<string> sorted_words;
    for (auto it=m.begin(); it!=m.end(); it++)
        sorted_words.push_back(it->first);
    sort(sorted_words.begin(), sorted_words.end());
    return sorted_words;
}
"""
	def functionsh(self):
		return """
/* 
 * File:   functions.h
 * Author: Lucas Reynolds
 * Section 2 Project 7
 * March 17, 2014
 */

#ifndef FUNCTIONS_H
#define	FUNCTIONS_H

#include<string>
using std::string;
#include<vector>
using std::vector;
#include<map>
using std::map;
#include<iterator>
using std::iterator;
#include<algorithm>
using std::find;

string lower_and_strip(string s);
void read_stopwords(vector<string> &, string file_name);
void read_file(map<string, long> &, vector<string> &, string file_name);
string print_map(map<string, long> &, string order="alpha");
vector<string> sorted_words(map<string, long> &);

template<typename Itr1, typename Itr2, typename Out> 
void my_set_intersection(Itr1 source1_begin, Itr1 source1_end, Itr2 source2_begin, 
                         Itr2 source2_end, Out dest) {
    /* find looks in source2 for what source1_it is pointing to
     * if two values are in both containers add one to the dest container and increment accordingly.*/
    for(auto source1_it=source1_begin; source1_it!= source1_end; source1_it++) {
        if(find(source2_begin, source2_end, *source1_it) != source2_end) {
            *dest = *source1_it;
            dest++;
        }
    }
}

template<typename Itr1, typename Itr2, typename Out>
void my_set_difference(Itr1 source1_begin, Itr1 source1_end, Itr2 source2_begin,
                       Itr2 source2_end, Out dest) {
    /* if one value is one of them but not the other
     * add value to dest container and increment accordingly 
     * why is this !=source1_end? yields same results as std::set_difference */
    for(auto source1_it=source1_begin; source1_it!= source1_end; source1_it++) {
        if(find(source2_begin, source2_end, *source1_it) != source1_end) {
            *dest = *source1_it;
            dest++;
        }
    }
}

#endif	/* FUNCTIONS_H */
"""
	def jobc(self):
		return """
/* 
 * File:   job.cpp
 * Author: Lucas Reynolds
 * Section 2 Project 9
 * April 7, 2014
 */

#include "job.h"

int Job::get_job_id() {
    return Job_Id_;
}

int Job::get_arrival_time() {
    return Arrival_Time_;
}

int Job::get_time_left() {
    return Service_Time_;
}

void Job::update_time_left(int time) {
    Service_Time_ -= time;
}

void Job::set_finish_time(int time) {
    Finish_Time_ = time;
}

int Job::get_finish_time() {
    return Finish_Time_;
}
"""
	def jobh(self):
		return """
/* 
 * File:   job.h
 * Author: Lucas Reynolds
 * Section 2 Project 9
 * April 7, 2014
 */

#ifndef JOB_H
#define	JOB_H

class Job {
private:
    int Job_Id_;
    int Arrival_Time_;
    int Service_Time_;
    int Finish_Time_;
public:
    Job() = default;
    Job(int j, int a, int s): Job_Id_(j), Arrival_Time_(a), Service_Time_(s) {};
    
    int get_job_id();
    int get_arrival_time();
    int get_time_left();
    void update_time_left(int time);
    void set_finish_time(int time);
    int get_finish_time();
};

#endif	/* JOB_H */
"""
	def madlibc(self):
		return """
/* 
 * File:   madlib.cpp
 * Author: Lucas Reynolds
 * Section 2 Project 5
 * February 24, 2014
 */

#include <vector>
#include <string>
#include <random>
#include <fstream>
#include <sstream>

using std::vector; using std::string; using std::getline;
using std::default_random_engine; using std::uniform_int_distribution;
using std::ifstream; using std::ofstream; using std::stringstream;
using std::istream_iterator; using std::back_inserter; using std::copy; using std::ispunct;

vector <string> load_word_file(string filename) {
    /* Reads a file with whitespaces
     * Returns a vector of words
     * If the filename doesn't work then the function will return an empty vector
     */
    string line;
    ifstream file;
    file.open(filename);
    vector <string> words;
    if(file.is_open()) {
        while (getline(file, line)) {
            if (line.empty() || line == " ") break;  //probably not needed especially empty
            stringstream stream (line);
            copy(istream_iterator<string>(stream), istream_iterator<string>(), back_inserter(words));
        }
    }
    file.close();
    return words;
}

string random_word(vector <string> &words, default_random_engine &dre) {
    /* Returns a random word from the vector of words 
     */
    uniform_int_distribution<long> dist(0, words.size()-1);
    return words.at(dist(dre));
}

void split(string line, vector <string> &vect) {
    /* Takes a string, returns a vector of the things separated by whitespaces
     * Similar to load_word_file expect this function takes a string instead of a filename that opens a file.
     */
    stringstream stream (line);
    copy(istream_iterator<string>(stream), istream_iterator<string>(), back_inserter(vect));
}

void process_document(string noun_file, string verb_file, string in_file, string out_file, int seed) {
    /* opens in_file and call load_word_file
     * replaces noun blanks with random nouns
     * replaces verb blanks with random verbs
     * writes the new line (or each element+spacing) to out_file
     */
    vector <string> nouns, verbs, story;
    default_random_engine dre(seed);
    nouns = load_word_file(noun_file);
    verbs = load_word_file(verb_file);
    story = load_word_file(in_file);
    
    for(int i=0; i<story.size(); i++) {
        if (story.at(i) == "<noun>")
            story.at(i) = random_word(nouns, dre);
        if (story.at(i) == "<verb>") // else if just adds an else statement that does nothing.
            story.at(i) = random_word(verbs, dre);
    }

    ofstream outfile (out_file);
    for(auto element : story) {
       if(ispunct(element[element.length()-1])) // if last char is punctuation make a new line
            outfile << element + "\n";
       else
            outfile << element + " ";
    }
    outfile.close();
}
"""
	def madlibh(self):
		return """
/* 
 * File:   madlib.h
 * Author: Lucas Reynolds
 * Section 2 Project 5
 * February 24, 2014
 */

#ifndef MADLIB_H
#define	MADLIB_H
#include <string>
#include <vector>
#include <random>

using std::vector; using std::string; using std::default_random_engine;

vector <string> load_word_file(string filename);
string random_word(vector <string> &, default_random_engine &);
void split(string, vector <string> &);
void process_document(string noun_file, string verb_file, string in_file, string out_file, int seed=98765);

#endif	/* MADLIB_H */
"""
	def marketc(self):
		return """
/* 
 * File:   market.cpp
 * Author: Lucas Reynolds
 * Section 2 Project 8
 * March 31, 2014
 */

#include "market.h"

#include <vector>
using std::vector;
#include <map>
using std::map;
#include <fstream>
using std::ifstream;
#include <string>
using std::string;
#include <algorithm>
using std::find;
#include <iterator>
using std::iterator; using std::distance;

Market::Market(string file_name) {
    // always initiated with constructor so this is the default.
    // each stock object has a long date and a vector of 30 doubles
    long date;
    double nums;
    ifstream infile;
    infile.open(file_name);
    if(infile.is_open()) {
        while (infile >> date) {
            vector<double> v;
            for (int i = 0; i < 30; i++) {
                infile >> nums;
                v.push_back(nums);
            }
            stocks[date] = v;
        }
    }
    infile.close();
}

double Market::get_price(string stock, long date) {
    /* returns the price of the stock on the date if: 
     * the date is valid, valid dates are in the stock keys.
     * the stock symbol is valid, valid symbols in the vector
     * and same positioning as the vector in stock.
     */
    vector<string> symbols = {"AA", "AXP", "BA", "BAC", "CAT", "CSCO", "CVX",
                   "DD", "DIS", "GE", "HD", "HPQ", "IBM", "INTC", "JNJ", "JPM",
                   "KFT", "KO", "MCD", "MMM", "MRK", "MSFT", "PFE", "PG", "T", 
                   "TRV", "UTX", "VZ", "WMT", "XOM"};
    
    auto it = find(symbols.begin(), symbols.end(), stock);
    if (it != symbols.end() && stocks.count(date) == 1) {
        auto index = distance(symbols.begin(), it);
        return stocks[date][index];
    }
    else
        return -1.0;
}
"""
	def marketh(self):
		return """
/* 
 * File:   market.h
 * Author: Lucas Reynolds
 * Section 2 Project 8
 * March 31, 2014
 */

#ifndef MARKET_H
#define	MARKET_H

#include <vector>
using std::vector;
#include <map>
using std::map;
#include <fstream>
using std::ifstream;
#include <string>
using std::string;

struct Market{
    map<long, vector<double>> stocks;
    
    // constructor that takes a single string argument, file name - dow.txt, and fills stocks
    // does constructor mess up defaults
    Market(string file_name);
    double get_price(string stock, long date);
};


#endif	/* MARKET_H */
"""
	def playerc(self):
		return """
/* 
 * File:   player.cpp
 * Author: Lucas Reynolds
 * Section 2 Project 8
 * March 31, 2014
 */

#include "player.h"
#include "market.h"

#include <vector>
using std::vector;
#include <map>
using std::map;
#include <string>
using std::string;
#include <sstream>
using std::ostringstream;
#include <iterator>
using std::iterator;
#include <iostream>
using std::endl;

// check stocks[thing] <<<-----

bool Player::buy(Market &m, string stock, long date, long quantity) {
    /* True if player has enough cash, valid symbol out of the 30, does purchasing
     * cash reduced, map stocks updated
     * False, does nothing
     */
    if (m.get_price(stock, date) != -1 && cash - m.get_price(stock, date) * quantity >= 0) {
        cash -= m.get_price(stock, date) * quantity;
        stocks[stock] += quantity;
        return true;
    }
    return false;
}

bool Player::sell(Market &m, string stock, long date, long quantity) {
    /* True if player has stock and quanity of stock
     * cash is increased, map stocks updated
     * False, nothing.
     * [stock] affects the output.
     */
    if (m.get_price(stock, date) != -1 && stocks[stock] >= quantity) {
        cash += m.get_price(stock, date) * quantity;
        stocks[stock] -= quantity;
        return true;
    }
    return false;
}

string Player::to_str() {
    // Player has:184.57 dollars, Stocks are:
    // symbol, quantity num
    ostringstream ostream;
    ostream << "Player has:" << cash << " dollars, Stocks are:" << endl;
    for(auto it = stocks.begin(); it != stocks.end(); it++)
        ostream << it->first << ", quantity " << it->second << endl;
    return ostream.str();
}
"""
	def playerh(self):
		return """
/* 
 * File:   player.h
 * Author: Lucas Reynolds
 * Section 2 Project 8
 * March 31, 2014
 */

#ifndef PLAYER_H
#define	PLAYER_H

#include "market.h"

#include <vector>
using std::vector;
#include <map>
using std::map;
#include <string>
using std::string;

struct Player {
    double cash;
    map<string, long> stocks;
    
    Player(double c) : cash(c) {}
    
    bool buy(Market &m, string stock, long date, long quantity);
    bool sell(Market &m, string stock, long date, long quantity);
    string to_str(); // Player has:184.57 dollars, Stocks are:
};

#endif	/* PLAYER_H */
"""
	def proj04c(self):
		return """
/* 
 * File:   proj03.cpp
 * Author: Lucas Reynolds
 * Section 2 Project 4
 * February 17, 2014
 */

#include<stdlib.h>
#include<iostream>
#include<string>

using std::cout; using std::endl; using std::cin;
using std::string; using std::stol; using std::to_string;

long rev_num(long n) {
    /* Reverse number by converting to a string 
     * and adds the number to the front of the string*/
    string num = to_string (n), number="";
    for(auto ch : num) {
        number = ch + number;
    }
    return stol(number);
}

bool is_palindrome(long n) {
    /* If the reverse and normal number are the same then return true. False otherwise.*/
    if (rev_num(n) == n)
        return true;
    else
        return false;
}

void order_parameters(long &first, long &second) {
    /* If the first is greater than the second, then swap the numbers.
     * Otherwise do nothing.*/
    if (first > second) {
        long temp = first;
        first = second;
        second = temp;
    }
}

bool check_lychrel(long n, long limit) {
    /* Is not given any natural palindromes. 
     * Adds the reverse number and regular number together.
     * Returns false if it can find a palindrome within the limit.
     * True if the number is a lychrel. */
    for (int i=0; i < limit; i++) { 
        n += rev_num(n);
        if (is_palindrome(n)) { 
            return false;
        }
    }
    return true;
}

long check_range(long start, long end, long limit, long &natural_cnt, long &pal_cnt) {
    /* Iterates through every number inbetween the valid range given or corrected.
     * Count = lychrel ctn. Natural count and palindrome are reference variables.
     * Adds 1 to the ctn/count it finds.
     */
    order_parameters(start, end);
    long count = 0;
    for (long s = start; s <= end; s++) {
        if (is_palindrome(s)) {
            natural_cnt += 1;
        }
        else if (!check_lychrel(s, limit)) {
            pal_cnt += 1;
        }
        else {
            cout << "Found a lychrel number: " << s << endl;
            count += 1;
        }
    }
    return count;
}

int main() {
    /* Prompts for first, last, and limit.
     * Calls the check_range once it has three variables that are >= 1.
     * Prints results.
     */
    long first=0, last=0, limit=0, natural_cnt=0, pal_cnt=0, lychrel_cnt=0;
    
    cout << "Provide first, last, and limit (all greater than one):";
    cin >> first >> last >> limit;
    if (first < 1 || last < 1 && limit < 1) {
        cout << "Try again, provide first, last, and limit (all greater than one):";
        cin >> first >> last >> limit;
    }
        
        
    lychrel_cnt = check_range(first, last, limit, natural_cnt, pal_cnt);
    cout << "Summary for range " << first << ", " << last << " with limit: " << limit << endl;
    cout << "Lychrel count: " << lychrel_cnt << ", Natural count: " << natural_cnt 
         << ", Palindrome count: " << pal_cnt << endl;
}
"""
	def proj05(self):
		return """
#######################################################################
# Section 11
# Computer Project #5
#######################################################################

# Split at tab and takes the first 5.  Then converts to the right type.
def get_crater_tuple(line_str):
    temp_list = []     # Temporary List ends up being tuple in master list.
    temp_list = line_str.split('\t')
    # Change to int, str, float, float, float. Rounds to two even though it's usually just one decimal.
    temp_list = temp_list[:5]
    temp_list[0] = int(temp_list[0])
    for i in range(2, 5):
        temp_list[i] = round(float(temp_list[i]), 2)
    return temp_list

# Trys to read file, then sorts the lines it gives to get_crater_tuple, then adds the tuple to the master_list.
def read_craters(filename):
    while True:
        try:
            file_pointer = open(filename, "r")  
            break
        except IOError:
            filename = input("Re-enter the file name: ")
        except FileNotFoundError:
            filename = input("Re-enter the file name: ")
    master_crater_list = []  # Contains each tuple, ends up being crater_list
    for line in file_pointer:
        if line[:1] in '123456789':
            master_crater_list.append(get_crater_tuple(line))
    file_pointer.close()
    return master_crater_list

# If the line meets the requirements then it's added to the new_crater_list
def get_eligible_craters(crater_list):
    i = 0
    new_crater_list = []  # Final crater list or eligible_crater_list, it adds only the eligible tuples.
    while i < len(crater_list):
        list_used_comparing = crater_list[i]
        if (-40 <= list_used_comparing[2] and list_used_comparing[2] <= 50) and (40 <= list_used_comparing[3] and list_used_comparing[3] <= 135) and list_used_comparing[4] >= 60:
            new_crater_list.append(list_used_comparing)
        i += 1
    return new_crater_list

# Writes the eligible_crater_list to the file craters.txt
def write_craters(eligible_crater_list):
    craters = open("craters.txt", "a+")
    for i in range(0, len(eligible_crater_list)):
        temp_writing_list = eligible_crater_list[i]  # Temporary writing list is each tuple in eligible_crater_list which is written to the file.
        craters.write("{:>3} {:<15} {:>9.2f} {:>9.2f} {:>9.2f}\n".format(temp_writing_list[0], temp_writing_list[1], temp_writing_list[2], temp_writing_list[3], temp_writing_list[4]))
    craters.close()
    return

# Opens a new crater.txt file and writes the first line, then it calls the function which do the work. 
craters = open("craters.txt", "w")
craters.write(" ID     Name         Latitude Longitude  Diameter\n")
craters.close()
file = input("Enter your file name: ")
crater_list = read_craters(file)
eligible_crater_list = get_eligible_craters(crater_list)
write_craters(eligible_crater_list)
"""
	def proj06(self):
		return """
###################################################################
# Section 10
# Computer Project 6
###################################################################


try:
    file = open("bestsellers.txt", "r")
    master_best_sellers_list = []
    for line in file:
        master_best_sellers_list.append(line.split('\t'))
    file.close()
except IOError:
    quit()
except FileNotFoundError:
    quit()
    
# Given two years, finds all the books inbetween the two years
def year_range(year1, year2, master_list):
    collection_of_titles_between = []
    for i in range(len(master_list)):
        temp_year = master_list[i][3].split('/')
        temp_year = int(temp_year[2].strip())
        if temp_year >= int(year1) and temp_year <= int(year2):
            collection_of_titles_between.append(master_list[i])
    return collection_of_titles_between

# Given month and year, finds all the books in the month of the year
def month_and_year(month, year, master_list):
    collection_of_monthyear = []
    for i in range(len(master_list)):
        temp_date_list = master_list[i][3].split('/')
        if int(temp_date_list[0]) == int(month) and int(temp_date_list[2].strip()) == int(year):
            collection_of_monthyear.append(master_list[i])
    return collection_of_monthyear

# Given a string it finds all authors that have that string, regardless of case.
def search_for_author(author_str, master_list):
    collection_of_author = []
    for i in range(len(master_list)):
        if author_str in master_list[i][1].lower():
            collection_of_author.append(master_list[i])
    return collection_of_author

# Given string finds all the titles that contain that string, regardless of case.
def search_for_title(title_str, master_list):
    collection_of_titles = []
    for i in range(len(master_list)):
        if title_str in master_list[i][0].lower():
            collection_of_titles.append(master_list[i])
    return collection_of_titles

# Easier than writing it out each time
def printing_function(collection_list):
    for i in range(len(collection_list)):
        print("    {:}, by".format(collection_list[i][0].strip()), collection_list[i][1].strip(), "({:})".format(collection_list[i][3].strip()))
    print()
    return

menu_list = ["Look up year range", "Look up month/year", "Search for author", "Search for title"]

while True:
    print("What would you like to do:")
    for i in range(1, 5):
        print("{:>1}:".format(i), menu_list[i-1])
    print("Q: Quit")
    user_choice = input(">")
    
    if user_choice.lower() == 'q':
        break

    # Year
    # Makes sure input is correct, then plugs it into the function, then that goes in the print function.
    if user_choice == '1':
        while True:
            try:
                beginning_year = input("Enter the beginning year: ")
                if len(beginning_year) == 4 and int(beginning_year) >= 1940 and int(beginning_year) <= 2013:
                    break
            except ValueError:
                beginning_year = input("Enter the beginning year: ")
        while True:
            try:
                ending_year = input("Enter the ending year: ")
                if len(ending_year) == 4 and int(ending_year) >= 1940 and int(ending_year) <= 2013 and ending_year >= beginning_year:
                    break
            except ValueError:
                users_year = input("Enter the ending year: ")
        titles_between_years_list = year_range(beginning_year, ending_year, master_best_sellers_list)
        if titles_between_years_list == []:
            print("\nThere were no titles between", beginning_year, "and", ending_year, "\n")
        else:
            print("\nAll the best sellers between", beginning_year, "and", ending_year + ':')
            printing_function(titles_between_years_list)
        
    # Month/Year            
    if user_choice == '2':
        while True:
            try: 
                users_month = input("Enter the month: ")
                if int(users_month) <= 12 and int(users_month) >= 1:
                    break
            except ValueError:
                users_month = input("Enter the month: ")
        while True:
            try:
                users_year = input("Enter the year: ")
                if len(users_year) == 4 and int(users_year) >= 1940 and int(users_year) <= 2013:
                    break
            except ValueError:
                users_year = input("Enter the year: ")
        list_of_best_sellers = month_and_year(users_month, users_year, master_best_sellers_list)
        if list_of_best_sellers == []:
            print("\nThere were no books in that particular month and year\n")
        else:
            print("\nAll the best sellers in month", users_month, "of", users_year + ':')
            printing_function(list_of_best_sellers)

    # Author
    if user_choice == '3':
        while True:
            try:
                users_author = input("Enter an author's name (or part of the name): ")
                author_list = search_for_author(users_author.lower(), master_best_sellers_list)
                if author_list == []:
                    print("\nThere were no authors with: " + users_author + "\n")
                    break
                else:
                    print("\nAll titles with the author's name " + users_author.capitalize() + ':')
                    printing_function(author_list)
                    break
            except ValueError:
                user_author = input("Enter an author's name (or part of the name): ")

    # Title
    if user_choice == '4':
        while True:
            try:
                users_title = input("Enter a title (or part of a title): ")
                title_list = search_for_title(users_title.lower(), master_best_sellers_list)
                if title_list == []:
                    print("\nThere were no titles with: " + users_title + '\n')
                    break
                else:
                    print("\nAll titles with " + users_title.capitalize() + ':')
                    printing_function(title_list)
                    break
            except ValueError:
                user_author = input("Enter a title (or part of a title): ")
"""
	def proj07(self):
		return """
def print_data(dictionary, county):
    print("\n" + county.title() + " County")
    print("   Count of people age 0-17 in poverty is {:}".format(dictionary[county][0]))
    print("   Percentage of people age 0-17 in poverty is {:}%".format(dictionary[county][1]))
    print("   The median household income is ${:5,d}\n".format(int(dictionary[county][2])))
    
# Highest percentage of children in poverty. Prints percentage, count of children, and median
# Creates two lists, one containing percentage and another containing percentage and name.
# Uses max to find the highest percentage, and then finds it in the second list.
def print_highest_data(dictionary):
    tl_percentage = []
    tl_percent_county = []
    for county in dictionary:
        tl_percent_county.append([float(dictionary[county][1]), county])
        tl_percentage.append(float(dictionary[county][1]))
    for nested_list in tl_percent_county:
        if nested_list[0] == max(tl_percentage):
            highest_percentage_county = nested_list[1]
    print_data(dictionary, highest_percentage_county)

# Same logic as above excepts uses min to find the lowest percentage of children in poverty.
def print_lowest_data(dictionary):
    tl_percentage = []
    tl_percent_county = []
    for county in dictionary:
        tl_percent_county.append([float(dictionary[county][1]), county])
        tl_percentage.append(float(dictionary[county][1]))
    for nested_list in tl_percent_county:
        if nested_list[0] == min(tl_percentage):
            lowest_percentage_county = nested_list[1]
    print_data(dictionary, lowest_percentage_county)

# Continually prompts for a county then it calls print_data
# Isn't case sensitive but it must be the full name of the county, not including 'county'.
# And needs . if necessary.
# Q or quit to go back to the menu.
def print_county_data(dictionary):
    while True:
        county_choice = input("Which County (Or Q): ").lower()
        if county_choice == 'q' or county_choice == "quit": break
        if county_choice.title() in dictionary:
            print_data(dictionary, county_choice.title())

# Opens the file, makes dictionary, calls desired function or quits.
# Assumes that est11_mi.txt exists.
def main():
    try:
        file_pointer = open("est11_mi.txt", "r")
    except FileNotFoundError:
        print("Error")
        quit()
    except IOError:
        print("Error")
        quit()

    c_dict = {}
    for line in file_pointer:
        county = line[193:238].strip()
        if county == 'Michigan': continue
        county = county[:-7]
        county_info = line.strip().split()
        c_dict[county] = county_info[8], county_info[11], county_info[20]

    file_pointer.close()
    
    while True:
        print("1: To find the highest percentage of children in poverty")
        print("2: To find the lowest percentage of children in poverty")
        print("3: To be continually prompted for a county")
        print("Q to Quit")
        answer = input(">")
        if answer == '1':
            print_highest_data(c_dict)
        if answer == '2':
            print_lowest_data(c_dict)
        if answer == '3':
            print_county_data(c_dict)
        if answer.lower() == 'q' or answer.lower() == 'quit': break

main()
"""
	def proj08(self):
		return """
##################################################################
#  Section 10
#  Computer Project #8
##################################################################
#  Project Overview:
#  To play freecell solitaire
#       Prints instructions and gameboard
#       Ask for a command which is either to try to moves a card, help, or quit.
#       Tries to do the command.  If it can't it prints an error. Then it reprints the correct board.
#       Asks for another command, repeats until the player quits, loses, or wins.
#


import cards

def setup():
    '''
    paramaters: None (deck can be created within this function)
    returns:
    - a foundation (list of 4 empty lists)
    - cell (list of 4 empty lists)
    - a tableau (a list of 8 lists, the dealt cards)
    '''
    deck = cards.Deck()
    deck.shuffle()
    foundation = [[], [], [], []]
    cell = [[], [], [], []] 
    tableau = []

    c = 1
    # Makes four rows of 7, four rows of 6
    while not deck.is_empty():
        nested_l = []
        if c <= 4:
            for i in range(7):
                nested_l.append(deck.deal())
        else:
            for i in range(6):
                nested_l.append(deck.deal())
        tableau.append(nested_l)
        c += 1

    return foundation,tableau,cell


def move_to_foundation(tableau, foundation, t_col, f_col):
    '''
    parameters: a tableau, a foundation, column of tableau, column of foundation
    returns: Boolean (True if the move is valid, False otherwise)
    moves a card at the end of a column of tableau to a column of foundation
    is also be used for c2f.
    '''
    # If list is empty return False
    try:
        t_card = tableau[t_col].pop()
    except IndexError:
        return False

    # foundation is blank and the card is an ace, append the card to the foundation list.
    if foundation[f_col] == []:
        if t_card.get_rank() == 1:
            foundation[f_col].append(t_card)
            return True
        else:
            tableau[t_col].append(t_card)
            return False
    else:
        f_card = foundation[f_col].pop() # Pops card because it passes first condition. Adds the card to the list if valid.
        if t_card.get_suit() == f_card.get_suit() and t_card.get_rank() == (f_card.get_rank() + 1):
            foundation[f_col].extend([f_card, t_card])
            return True
        else:
            foundation[f_col].append(f_card)
            tableau[t_col].append(t_card)
            return False


def move_to_cell(tableau,cell,t_col,c_col):
    '''
    parameters: a tableau, a cell, column of tableau, column of cell
    returns: Boolean (True if the move is valid, False otherwise)
    moves a card at the end of a column of tableau to a cell
    '''
    if cell[c_col] == []:  
        cell[c_col].append(tableau[t_col].pop())
        return True
    return False # Would return false without this.
    
def move_to_tableau(tableau, cell, c_col, t_col):
    '''
    parameters: a tableau, a cell, column of tableau, a cell
    returns: Boolean (True if the move is valid, False otherwise)
    moves a cards in the cell to a column of tableau
    checks the validity of move
    '''
    color = {1: 'black', 2: 'red', 3: 'red', 4: 'black'}

    if cell[c_col] == []:
        return False
    elif tableau[t_col] == []:
        tableau[t_col].append(cell[c_col].pop())
        return True
    else:
        t_card = tableau[t_col].pop()
        c_card = cell[c_col].pop()

        if (t_card.get_rank() - 1) == c_card.get_rank() and color[t_card.get_suit()] != color[c_card.get_suit()]:
            tableau[t_col].extend([t_card, c_card])
            return True
        else:
            tableau[t_col].append(t_card)
            cell[c_col].append(c_card)
            return False

def is_winner(foundation):
    '''
    parameters: a foundation
    return: Boolean
    Checks to see if the player won.
    Starts with false, if the last card in each stack of foundations is a king it returns trues.
    '''
    is_winner = False
    try:
        slot1 = foundation[0][-1]
        slot2 = foundation[1][-1]
        slot3 = foundation[2][-1]
        slot4 = foundation[3][-1]
        # if all contain kings it changes is_winner to True. IndexError catches the empty lists.
        if slot1.get_rank() == 13 and slot2.get_rank() == 13 and slot3.get_rank() == 13 and slot4.get_rank() == 13:
            is_winner = True
    except IndexError:
        pass
    return is_winner


def move_in_tableau(tableau, t_col_source, t_col_dest):
    '''
    parameters: a tableau, the source tableau column and the destination tableau column
    returns: Boolean
    moves a card from one tableau column to another
    remember to check validity of move'''

    color = {1: 'black', 2: 'red', 3: 'red', 4: 'black'}  # Uses .get_suit() and then finds the color. 
    
    if tableau[t_col_dest] == [] and tableau[t_col_source] != []:
        tableau[t_col_dest].append(tableau[t_col_source].pop())
        return True
    elif tableau[t_col_source] == []:
        return False
    else:
        t_s_card = tableau[t_col_source].pop()
        t_d_card = tableau[t_col_dest].pop()

        if (t_s_card.get_rank() + 1) == t_d_card.get_rank() and color[t_s_card.get_suit()] != color[t_d_card.get_suit()]:
            tableau[t_col_dest].extend([t_d_card, t_s_card])
            return True
        else:
            tableau[t_col_source].append(t_s_card)
            tableau[t_col_dest].append(t_d_card)
            return False

def move_all_valid_to_foundation(tableau, cell, foundation):
    '''
    Moves all valid cards to the foundation, when list has collected all false it stops.
    '''
    validation_list = []
    for i in range(12):
        validation_list.append(True)
        
    while True in validation_list:
        i = 0
        while i < 8:
            valid1 = move_to_foundation(tableau, foundation, i, 0)
            valid2 = move_to_foundation(tableau, foundation, i, 1)
            valid3 = move_to_foundation(tableau, foundation, i, 2)
            valid4 = move_to_foundation(tableau, foundation, i, 3)
            valid_list = [valid1, valid2, valid3, valid4]
            if True in valid_list:
                validation_list[i] = True
            else:
                validation_list[i] = False
                print
            i += 1
            c = 0
        while c < 4:
            valid1 = move_to_foundation(cell, foundation, c, 0)
            valid2 = move_to_foundation(cell, foundation, c, 1)
            valid3 = move_to_foundation(cell, foundation, c, 2)
            valid4 = move_to_foundation(cell, foundation, c, 3)
            valid_list = [valid1, valid2, valid3, valid4]
            if True in valid_list:
                validation_list[c+8] = True
            else:
                validation_list[c+8] = False
            c += 1

def move_all_valid_cards_in_tableau(tableau, cell, t_col, o_col):
    count = 4
    open_cells = []
    for c in cell:
        if c != []:
            open_cells.append(cell.index(c))
            print(cell.index(c))
            move_to_cell(tableau, cell, t_col, cell.index(c))

    if open_cells == []:
        if not move_in_tableau(tableau, t_col, o_col):
            return False
        return True
    else:
        open_cells = open_cells.reverse()
        print(open_cells)
        for num in open_cells:
            if not move_to_tableau(tableau, cell, open_cells[num], o_col):
                move_to_tableau(tableau, cell, open_cells[num], t_col)
        if not move_in_tableau(tableau, t_col, o_col):
            return False
        return True
            
        
    
    
def print_game(foundation, tableau, cell):
    '''
    parameters: a tableau, a foundation and a cell
    returns: Nothing
    prints the game, i.e, print all the info user can see.
    Includes:
        a) print tableau  
        b) print foundation ( can print the top card only)
        c) print cells

    '''
    print()
    print("                 Cells:                              Foundation:")
    # print cell and foundation labels in one line
    for i in range(4):
        print('{:8d}'.format(i+1), end = '')
    print('    ', end = '')
    for i in range(4):
        print('{:8d}'.format(i+1), end = '')
    print()  # carriage return at the end of the line
    # print cell and foundation cards in one line; foundation is only top card
    for c in cell:
        # print if there is a card there; if not, exception prints spaces.
        try:
            print('{:>8s}'.format(c[0]), end = '')
        except IndexError:
            print('{:>8s}'.format(''), end = '')
            
    print('    ', end = '')
    for stack in foundation:
        # print if there is a card there; if not, exception prints spaces.
        try:
            print('{:>8s}'.format(stack[-1]), end = '')
        except IndexError:
            print('{:>8s}'.format(''), end = '')

    print()  # carriage return at the end of the line
    print('----------')

    print("Tableau")
    for i in range(len(tableau)):  # print tableau headers
        print('{:8d}'.format(i + 1), end = '')
    print()  # carriage return at the end of the line

    # Find the length of the longest stack
    max_length = max([len(stack) for stack in tableau])

    # print tableau stacks row by row
    for i in range(max_length):  # for each row
        print(' '*7, end = '')  # indent each row
        for stack in tableau:
            # print if there is a card there; if not, exception prints spaces.
            try:
                print('{:8s}'.format(stack[i]), end = '')
            except IndexError:
                print('{:8s}'.format(''), end = '')
        print()  # carriage return at the end of the line
    print('----------')

def print_rules():
    '''
    parameters: none
    returns: nothing
    prints the rules
    '''
    print("Rules of FreeCell")

    print("Goal")
    print("\tMove all the cards to the Foundations")

    print("Foundation")
    print("\tBuilt up by rank and by suit from Ace to King")

    print("Tableau")
    print("\tBuilt down by rank and by alternating color")
    print("\tThe bottom card of any column may be moved")
    print("\tAn empty spot may be filled with any card ")

    print("Cell")
    print("\tCan only contain 1 card")
    print("\tThe card may be moved")

def show_help():
    '''
    parameters: none
    returns: nothing
    prints the supported commands
    '''
    print("Responses are: ")
    print("\t t2f #T #F - move from Tableau to Foundation")
    print("\t t2t #T1 #T2 - move card from one Tableau column to another")
    print("\t t2c #T #C - move from Tableau to Cell")
    print("\t c2t #C #T - move from Cell to Tableau")
    print("\t c2f #C #F - move from Cell to Foundation")
    print("\t 'h' for help")
    print("\t 'q' to quit")
    
    
def play():
    '''
    parameters: none
    returns: nothing
    Main program. Does error checking on the user input. 
    '''
    print_rules()
    foundation, tableau, cell = setup() 
       
    show_help()
    while True:  # If the player loses (no moves left), it is assumed that the player gives up and quits.
        move_all_valid_to_foundation(tableau, cell, foundation)
        print_game(foundation, tableau, cell)
        response = input("Command (type 'h' for help): ")
        response = response.strip()
        response_list = response.split()
        if len(response_list) > 0 and len(response_list) <= 3:
            r = response_list[0]
            if r == 'q' or r == 'h':  # Does q and h seperately because it needs to seperate response_list.
                if r == 'q': break  #q and h can be followed by two 'words' and it will still call the function or break.
                else:               #But they're no other reasons to type in q or h then for it to call the function or break.
                    show_help()
            # special column numbers if response is t2t or c2t
            else:
                try: # t_num is the first number, which in most cases is for the tableau, o_num is for the second number
                    t_num = response_list[1]
                    o_num = response_list[2]
                    t_num = int(t_num) - 1
                    o_num = int(o_num) - 1
                except TypeError:
                    print("Error with input")
                    continue
                except IndexError:
                    print("Error with input")
                    continue
                except ValueError:
                    print("Error with input")
                    continue
                # Calls the desired function and makes sure that the input is valid. Numbers ranges are 0-7 and 0-3.
                if r == 't2f':
                    if 0 <= t_num < 8 and 0 <= o_num < 4:
                        if not move_to_foundation(tableau, foundation, t_num, o_num):
                            print("That move is invalid")
                    else:
                        print("Error with input")
                elif r == 't2t':
                    if 0 <= t_num < 8 and 0 <= o_num < 8:
                        if not move_in_tableau(tableau, t_num, o_num):
                            print("That move is invalid")
                    else:
                        print("Error with input")
                elif r == 'at2t':
                    if 0 <= t_num < 8 and 0 <= o_num < 8:
                        if not move_all_valid_cards_in_tableau(tableau, cell, t_num, o_num):
                            print("That move is invalid")
                    else:
                        print("Error with input")
                elif r == 't2c':
                    if 0 <= t_num < 8 and 0 <= o_num < 4:
                        if not move_to_cell(tableau, cell, t_num, o_num):
                            print("That move is invalid")
                    else:
                        print("Error with input")
                elif r == 'c2t':
                    if 0 <= t_num < 4 and 0 <= o_num < 8:
                        if not move_to_tableau(tableau, cell, t_num, o_num):
                            print("That move is invalid")
                    else:
                        print("Error with input")
                elif r == 'c2f':
                    if 0 <= t_num < 4 and 0 <= o_num < 4:
                        if not move_to_foundation(cell, foundation, t_num, o_num):
                            print("That move is invalid")
                    else:
                        print("Error with input")
                else:
                    print('Unknown command:',r)
        else:
            print("Unknown Command:",response)
        if is_winner(foundation):
            print("You won!!!") # Not worth it....
            break
    print('Thanks for playing')

play()
"""
	def proj09app(self):
		return """
##################################################################
#  Section 10
#  Computer Project #9
##################################################################
#  Project Overview:
#  App
#       Given input from proj09-input.txt.
#       For each line, print line number and validality.
#       If valid print area and perimeter
#       Find the number of lines processed, number of valid triangles,
#       average area, average perimeter, the triangle with the largest area, and
#       the triangle with largest perimeter.

import triangle
try:
    fp = open("proj09-input.txt")
except IOError:
    print("File cannot be found")
    exit()

lines_processed = 0
valid_triangles = 0
perimeters = 0
areas = 0
largest_perimeter = [0, 0, 0]
largest_area = [0, 0, 0]


for line in fp:
    lines_processed += 1
    sides = line.lstrip(" (")
    sides = sides.rstrip(' )\n')
    sides = sides.split(", ")  # Removes the parenthesis and \n, leaving a list containing the three sides.
    
    try:
        sides = [float(sides[0]), float(sides[1]), float(sides[2])]
        T = triangle.Triangle(sides[0], sides[1], sides[2])
        # converts to a float if it can.
    except ValueError:
        print("Line {:>2d}: {:}".format(lines_processed, line))
        print("\tTriangle is not valid\n")
        continue
    
    print("Line {:>2d}: {:}".format(lines_processed, line))
    if T.is_valid():
        valid_triangles += 1
        print("\tTriangle is valid, {:}".format(T))
        print("\tPerimeter: {:}".format(T.perimeter()))
        # Compares the new perimeter with the previous perimeter
        if T.perimeter() > triangle.Triangle(largest_perimeter[0], largest_perimeter[1], largest_perimeter[2])\
           .perimeter():
            largest_perimeter = [float(sides[0]), float(sides[1]), float(sides[2])]
        perimeters += T.perimeter()
        print("\tArea: {:}\n".format(T.area()))
        # Compares the new area with the previous area
        if T.area() > triangle.Triangle(largest_area[0], largest_area[1], largest_area[2]).area():
            largest_area = sides
        areas += T.area()
    else:
        print("\tTriangle is not valid\n")

print("Total number of lines processed: {:}".format(lines_processed))
print("Total number of valid triangles: {:}".format(valid_triangles))
# if zero triangles processed then this prints 0.  Avg. Area, Avg. Perimeter, Largest Perimeter, and Largest Area are defaulted as zero.
try:
    print("Average perimeter for all valid triangles: {:2f}".format(perimeters / valid_triangles))
    print("Average area for all valid triangles: {:2f}\n".format(areas / valid_triangles))
except ZeroDivisionError:
    print("Average perimeter for all valid triangles: 0")
    print("Average area for all valid triangles: 0")

l_perimeter_t = triangle.Triangle(largest_perimeter[0], largest_perimeter[1], largest_perimeter[2])
print("Valid triangle with the largest perimeter: {:}".format(l_perimeter_t))
print("  Triangle with largest perimeter, perimeter: {:.2f}".format(l_perimeter_t.perimeter()))
print("  Triangle with largest perimeter, area: {:.2f}\n".format(l_perimeter_t.area()))
      
l_area_t = triangle.Triangle(largest_area[0], largest_area[1], largest_area[2])
print("Valid triangle with the largest area: {:}".format(l_area_t))
print("  Triangle with largest area, perimeter: {:.2f}".format(l_area_t.perimeter()))
print("  Triangle with largest area, area: {:.2f}".format(l_area_t.area()))
"""
	def proj09test(self):
		return """
##################################################################
#  Section 10
#  Computer Project #9
##################################################################
#  Project Overview:
#  Test
#       Tests the class Triangle
#       Uses list containing different variables to test the class.
#       Variables include erroneous numbers/variables, valid numbers
#       Shows the functions isosceles, equilateral, and scalene.
#       Also shows negative factor, None angles, and Perimeter/Area = 0

import triangle

# Each nested list contains three sides, factor, and description.
test_list = [[10, 10, 10, 1000, "Equilateral Triangle, __str__, and scale"], [9, 5, 5, .5, "Isosceles Triangle"], [4, 6, 8, 10, "Scalene Triangle"], [1000, 12, 100312, 1, "An Invalid Triangle"],\
             [5.987, 8.50903524, 5.123, -3, "Decimals, when printing triangle it's only to one decimal place"],\
             ["a", "b", "c", 2, "Error Checking"], ["Hey", "Mom", "bye", 2, "Error Checking"], [0, 5, 5, 5, "One Side Equals Zero"], [0, 0, 0, 5, "All Sides Equal Zeros"]]

print("Triangle with no values: {}\n".format(triangle.Triangle()))

for sides in test_list:
    print("Demonstrates {}".format(sides[4]))
    A = triangle.Triangle(sides[0], sides[1], sides[2])
    print("Input ( {}, {}, {} ) into triangle.Triangle(x, x, x)".format(sides[0], sides[1], sides[2]))
    print("   Result: {:}".format(A))
    if sides[:3] == [10, 10, 10]:
        print("   Written with __str__: {:}".format(A.__str__()))
    print("   Triangle method is_valid and __validate: {:}".format(A.is_valid()))
    print("   Method Sides: {:}".format(A.sides()))
    print("   Method Angles: {:}".format(A.angles()))
    print("   Method Perimeter: {:}".format(A.perimeter()))
    print("   Method Area: {:}".format(A.area()))
    print("   Is an equilateral triangle: {:}".format(A.is_equilateral()))
    print("   Is an isosceles triangle: {:}".format(A.is_isosceles()))
    print("   Is a scalene triangle: {:}".format(A.is_scalene()))
    print("   Method Scale, Factor of {:}: {:}".format(sides[3], A.scale(sides[3])))
    if sides[:3] == [10, 10, 10]:
        print("   Triangle is now {}".format(A))
        print("   Method Sides: {:}".format(A.sides()))
        print("   Method Angles: {:}".format(A.angles()))
        print("   Method Perimeter: {:}".format(A.perimeter()))
        print("   Method Area: {:}".format(A.area()))
    print()
"""
	def proj10app(self):
		return '''
##################################################################
#  Section 10
#  Computer Project #10
##################################################################
#  Project Overview:
#  App
#       Prints a statement about this app's function
#       Creates a bank account with a 1000 USD
#       Repeatedly asks the user for a deduction and currency code
#       Prints the new amount after the deduction
#       Decucts money until the user enters q or the account is negative or zero.
#       Detects errors with the user's input

import currency

currency_mod = currency.Currency()

def print_instructions():
    """
    Prints instructions for this application.
    Parameters nothing. Returns nothing.
    """
    print("This application will create a bank account with 1000 USD.")
    print("After you will be asked to deduct money in the form XXX YYY")
    print("XXX is a dollar amount")
    print("YYY is a currency code (USD, EUR, SEK, CAD, CNY, and GBP)")
    print("The application will repeatedly prompt for an amount and currency code")
    print("Until you enter q or the account contains either zero dollars or negative dollars.\n")


def main(currency):
    """
    Creates two accounts one with 1000 USD and one with 0 USD.
    Repeatedly asks the user for an amount and
    currency code which it uses to decuct from the account with 1000.
    It also detects the users input for errors.
    Parameters nothing. Returns nothing.
    """
    
    print_instructions()

    c_curr = currency
    account = currency + 1000
    
    print("The Account is Initizalized at {:}".format(account))
    
    while account > c_curr:
        u_input = input(">>")
        if u_input.lower() == 'q':
            print("The Account is Finialized at: {:}".format(account))
            break
        u_input = u_input.split()
        try:
            if u_input[1] in ['USD', 'EUR', 'SEK', 'CAD', 'CNY', 'GBP']:
                try:
                    amount = float(u_input[0])
                    deduct_curr = currency.convert_to(u_input[1])
                    deduct_curr = amount
                    account = account - deduct_curr
                    print("The Account is {:}".format(account))
                except ValueError:
                    print("Error with Amount")
            else:
                print("Error with Input")
        except IndexError:
            print("Error with Input")
        if not account > c_curr:
            print("The Account is Overdrawn")

main(currency_mod)
'''
	def proj10test(self):
		return """
##################################################################
#  Section 10
#  Computer Project #10
##################################################################
#  Project Overview:
#  Test
#       Tests the class Currency
#       Creates 6 currency objects with each of the currencies that the programs has to use.
#       Two instances create the currency with the convert_to method
#       The display shows __repr__ and __str__ isn't shown because __str__ calls __repr__.
#       For addition and subtraction the program displays a currency +/- currency2
#       Then currency +/- int or float and int or float +/- currency
#       For greater than, this test shows that it returns true iff one currency is greater than the other.

import currency

A = currency.Currency()
print("A   Currency()              A: {:}".format(A))
B = currency.Currency(100, 'EUR')
print("B   Currency(100, '"'EUR'"')    B: {:}".format(B))
C = currency.Currency(1000, 'GBP')
print("C   Currency(1000, '"'GBP'"')   C: {:}".format(C))
D = B.convert_to('CAD')
print("D   B.convert_to('"'CAD'"')     D: {:}".format(D))
E = currency.Currency(90.123, 'CNY')
print("E   Currency(90.125, '"'CNY'"') E: {:}".format(E))
F = C.convert_to('SEK')
print("F   C.convert_to('"'SEK'"')     F: {:}".format(F))

print("\n   Addition")
print("A + B:   ", A + B)
print("C + 50.0:", C + 50.2)
print("50 + F:  ", 50 + F)

print("\n   Subtraction")
print("C - D:   ", C - D)
print("50.0 - A:", 50.5 - A)
print("F - 50:  ", F - 50)

print("\n   Greater than")
print("A > B: ", A > B)
print("E < D: ", E < D)
print("C > D: ", C > D)
"""
	def proj11(self):
		return '''
##################################################################
#  Section 10
#  Computer Project #11
##################################################################
#  Project Overview:
#       Make a game based of the Dilbert cartoon.
#       Player enters a number where they want their hook at.
#       Time limit goes and player catches a fish if the hook number and fish number align.

import random, math, turtle, urllib.request

##################################################################
## Class GameBoard
##################################################################

class GameBoard( object ):

    def __init__( self, squares_i=49, hook_location=1, speed=0, fish_list=None ):
        """
        Initializes the variables: squares, fish_list, fish_count, speed, and hook.
        Parameters have default variables.
        Returns nothing.
        """
        if fish_list == None: # in case urllib doesn't work correctly.
            self.__fish_list = [' Magikarp', ' Gyardos', ' Tynamo', ' Huntail', ' Lapras']
        else:
            self.__fish_list = fish_list
        # numinput and if statement does the error checking.
        self._fish_count = 0 
        self.__hook = int(hook_location)
        self.__squares = int(squares_i)
        self.__speed = int(speed)
                
    def __repr__( self ):
        """
        Returns a representation of the gameboard variables
        __str__ would call this, if repr had any value.
        """
        return "Gameboard Variables: Size:{:}, Squares:{:}, HL:{:}, FC:{:}".format(self.__board_size, self.__squares, self.__hook, self.__fish_count)

    def variables( self ):
        """
        Return: Squares, hook, fish_list, fish_count, speed
        """
        return self.__squares, self.__hook, self.__fish_list, self._fish_count, self.__speed
        
    
    def fish_count_update( self ):
        """
        This method is used to add one to fish count
        Return: Fish Count
        """
        self._fish_count += 1
        return self._fish_count

    def speed_update_i( self ):
        """
        Makes fish appear slower when called.
        Returns: None
        """
        if self.__speed != 10:
            self.__speed += 1
            self.time()
        
    def speed_update_d( self ):
        """
        Makes fish appear faster when called.
        Returns: None
        """
        if self.__speed != 0:
            self.__speed -= 1
            self.time()
        
    def time( self ):
        """
        Determines how long the game lasts.
        Returns: timer_len
        """
        if self.__speed == 0:
            self._timer_len = 0
        if self.__speed > 0 and self.__speed <= 4:
            self._timer_len = self.__speed * random.randint(1,100)
        elif self.__speed >= 5 and self.__speed < 6:
            self._timer_len = self.__speed * random.randint(100,300)
        elif self.__speed >= 7 and self.__speed < 10:
            self._timer_len = self.__speed * random.randint(300,3000)
        else:
            self._timer_len = self.__speed * random.randint(3000,10000)

    def timer_len( self ):
        """
        timer_len is a variable
        if timer_len isn't define it creates a new one.
        """
        try:
            return self._timer_len
        except AttributeError:
            self.time()
            return self._timer_len
   

def create_fish_list():
    """
    Uses urllib to go to website that has water pokemon
    Goes through the html code to find the pokemon names
    Adds a space and if the name starts with a vowel it adds a n
    The list doesn't include starter pokemon.
    Some protection in case it fails to work.
    Parameters: None
    Returns: A list of water pokemon, specifically 108.
    """
    
    try:
        web_obj = urllib.request.urlopen("http://pokemondb.net/type/water")
        result_str = str(web_obj.read())
        web_obj.close()

        result_str = result_str[result_str.find("/pokedex/"):]
        result_lst = result_str.split("<a href")
        
        pokemon = []
        for string in result_lst:     ## adds the strings that have pokemon in them in.
            if "/pokedex/" in string:
                pokemon.append(string)

        pokemon = pokemon[9:] # Gets rid of starter pokemon and titles
        pokemon_fishing_lst = []

        for pokemon_name in pokemon:
            name = pokemon_name[pokemon_name.find("/", 4)+1:]
            name = name[:name.find(' ')-1].capitalize()
            if name in ["Marshtomp", "Swampert", "Mudkip", "Totodile", "Croconaw", "Feraligatr",
            		    "Froakie", "Frogadier", "Greninja"]: continue
            if name[:1] in "AEIOU": # adds a space and a n to fix grammar
                name = "n "+name
            else:
                name = " "+name
            pokemon_fishing_lst.append(name)
            
        if len(pokemon_fishing_lst) < 70:
            return None
        
        return pokemon_fishing_lst
    except OSError:
        pass
    
def instructions():
    """
    Creates the first screen in a turtle window.
    Writes the instructions in the background.
    Prompts the user for Squares, Fishing Location, and Hook Location
    Assumes the user wants to enter correct numbers.
    Resets screen after.
    Parameters: None
    Returns: squares_int, fishing_location, hook_location
    """
    turtle.title("")
    turtle.bgcolor((.96, .96, .96))
    pen.up()
    pen.goto(0, 100)
    pen.write("Welcome to Carpet Fishing:", align="center", font=("Arial", 20, "normal"))
    pen.pencolor("red")
    pen.goto(0, 80)
    pen.write("Pokemon Black and White Edition", align="center", font=("Arial", 17, "bold"))
    pen.pencolor("black")
    pen.goto(0, 50)
    pen.write("Instructions:", align="center", font=("Arial", 18, "normal"))
    y_cord = 25 
    instruction_list = ["Enter a perfect square which will be used to divide the cubicle.",
                        "Select where to place the hook",
                        "Select the rate that fish appear.",
                        "Left Arrow Key to make fish appear faster.",
                        "Right Arrow Key to make fish appear slower.",
                        "Press Q to quit or Exit out of the screen."]
    
    for writing in instruction_list:
        pen.up()
        pen.goto(0, y_cord)
        pen.write(writing, align="center", font=("Arial", 15, "normal"))
        y_cord -= 30

    while True: 
        try:
            number_of_squares = int(turtle.numinput("Number of Squares", "Pick a number (Preferably a Perfect Square)"))
            if type(number_of_squares) == int and number_of_squares > 0: break  
        except TypeError:
            continue
    while True:
        try:
            hook = turtle.numinput("Hook Location", "Place the hook in which box (1-{:})".format(int(number_of_squares)))
            if hook <= number_of_squares and hook > 0: break
        except TypeError:
            continue
    while True:
        try:
            speed = turtle.numinput("Game Length", "Speed that fish appear at. 0-10 scale (0 is the fastest and an effective demo, 10 is the Slowest)")
            if speed >= 0 and speed <= 10: break
        except TypeError:
            continue
    
    return int(number_of_squares), int(hook), int(speed)

def draw_square( length, width, color, cord, is_fill=False ):
    """
    Uses turtle graphics to draw a square
    Can handle filling the square with a color such as blue
    Can also handle drawing a black border
    Must start at cordinates its cordinates
    """
    pen.ht()
    pen.speed(0)
    pen.goto(cord)
    pen.down()
    if is_fill:
        pen.fillcolor(color)
        pen.begin_fill()
    else:
        pen.pencolor(color)
    pen.forward(width)
    pen.right(90)
    pen.forward(length)
    pen.right(90)
    pen.forward(width)
    pen.right(90)
    pen.forward(length)
    pen.right(90)
    pen.forward(width)
    if is_fill:
        pen.end_fill()
    pen.up()

def draw_lines( number, hook_number ):

    num = 1
    num_list = []
    prev_num = 0
    for num in range(1,number):
        multi1 = number/num
        if not multi1 >  int(multi1):
            num_list.append([num, int(multi1)])
            if len(num_list) > 2:
                if num_list[-1][::-1] in num_list and num_list[-1][0] != num_list[-1][1]:
                    num_list.pop()
                    break
        num += 1
    numbers = max(num_list)

    pen.ht()
    pen.speed(7)
    start_cord = [-250, 250]
    y_interval, x_interval = 500/numbers[0], 500/numbers[1]
    pen.up()
    pen.goto(start_cord)
    pen.pd()
    pen.seth(0)
    pen.forward(500)
    pen.up()
    pen.goto(start_cord)
    pen.pd()
    pen.seth(270)
    pen.forward(500)
    
    for i in range(1, numbers[0]+1):
        pen.up()
        start_cord[1] = start_cord[1] - y_interval
        pen.goto(start_cord)
        pen.pd()
        pen.seth(0)
        pen.forward(500)
    
    start_cord [1] = 250
    for i in range(1, numbers[1]+1):
        pen.up()
        start_cord[0] = start_cord[0] + x_interval
        pen.goto(start_cord)
        pen.pd()
        pen.seth(270)
        pen.forward(500)

    r = 0
    c = hook_number
    while True:
        if (c - numbers[1]) > 0:
            c -= numbers[1]
            r += 1
        else: break

    cord = [(-250 + (c * x_interval)), (250 - (r * y_interval))]
    pen.up()
    pen.goto(cord)
    draw_square(x_interval, y_interval, "gray", cord, True)

def draw_board( gameboard ):
    """
    Sets up the game board, green background and a blue 500x500 board
    Draws the squares that is requested
    Draws other information on the board -fish count, speed
    """
    turtle.bgcolor("green")
    pen.ht()
    pen.up()
    pen.goto(0, 300)
    pen.write("Carpet Fishing", align="center", font=("Arial", 20, "bold"))
    squares, hook, fish_list, fish_count, speed = gameboard.variables()
    pen.speed(0)
    draw_square(500, 500, (0.3, 0.35, 1.00), (-250, 250), True)
    draw_lines(squares, hook)

    pen.pencolor("black") # writes fish count
    pen.goto(300, 235)
    pen.write("Fish Count", align="center", font=("Arial", 15, "underline"))
    pen.goto(300, 215)
    pen.write(fish_count, align="center", font=("Arial", 15, "normal"))
    
    pen.goto(300, 195) # writes speed
    pen.write("Speed", align="center", font=("Arial", 15, "underline"))
    pen.goto(300, 175)
    pen.write(speed, align="center", font=("Arial", 15, "normal"))
    
    pen.goto(-300, 235) # writes water pokemon
    pen.write("Water", align="center", font=("Arial", 15, "normal"))
    pen.goto(-300, 215)
    pen.write("Pokemon", align="center", font=("Arial", 15, "normal"))
            
def generate_fish( gameboard ):
    """
    Uses the gameboard to make a list of variables
    Every times this is called it generates a random number between 1 and the number of squares
    If hook aligns with that number, it uses turtle graphics to display the fish name and updates the total fish count.
    Calls draw_square to draw a white box overtop of what's original there.
    """
    squares, hook, fish_list, fish_count, speed = gameboard.variables()
    fish_loc = random.randint(1, squares)
    if fish_loc == hook:
        pen.speed(0)
        pen.ht()
        fish_name = fish_list[random.randint(0, len(fish_list)-1)]
        pen.up()
        pen.pencolor("green")
        draw_square(100, 500, 'green', (-250, -270), True)
        pen.goto(0, -300)
        pen.pencolor("black")
        pen.write("You caught a" + fish_name + "!", align="center", font=("Arial", 20, "normal"))
        pen.pencolor("green")
        draw_square(20, 40, 'green', (280, 235), True)
        pen.goto(300, 215)
        pen.pencolor("black")
        pen.write(gameboard.fish_count_update(), align="center", font=("Arial", 15, "normal"))

def update_speed(speed):
    """
    When the player changes the speed
    Draws a box to clear the previous speed and writes the new speed
    Parameter: Speed, Return: None
    """
    pen.up()
    pen.ht()
    pen.pencolor("green")
    draw_square(20, 30, 'green', (290, 195), True)
    pen.goto(300, 175)
    pen.pencolor("black")
    pen.write(speed, align="center", font=("Arial", 15, "normal"))

def refresh_screen():
    """
    Parameters: None, Return: None
    Draws a green box around the bottom of the screen when fish haven't appeared in a while.
    """
    pen.up()
    pen.ht()
    pen.pencolor("green")
    draw_square(100, 500, 'green', (-250, -270), True)
    
def main():
    """
    Prints the instructions in turtle
    graphics and prompts the user for variables.
    Creates a gameboard with those variables
    Uses the gameboard to simiulate carpet fishing.
    Parameters:None
    Return:None
    """
    fish_list = create_fish_list()
    squares, hook, speed = instructions()
    A = GameBoard(squares, hook, speed, fish_list)
    
    pen.reset()
    draw_board(A)
    pen.ht()
    count = 1

    while True:
        turtle.onkey(quit, "q")
        turtle.onkey(quit, "Q")
        turtle.onkey(A.speed_update_i, "Right")
        turtle.onkey(A.speed_update_d, "Left") # Q to quit, Right/Left to adjust speed
        turtle.listen()
        
        a, b, c, d, speed1 = A.variables()
        if speed != speed1: # changes the speed info on the gui and the class
            speed = speed1
            update_speed(speed)
            count = 0
        if speed == 0:  # special case, rapidly produces fish
            generate_fish(A)
            continue
        
        if A.timer_len != 0:
            if count % A.timer_len() == 0:
                generate_fish(A)
                count = 0
                A.time()
        else:
            generate_fish(A)
            count = 0
            
        if count >= 300:
            refresh_screen()
        count += 1
        

       
pen = turtle.Turtle()
pen.speed(0)
pen.ht()
main()
'''
 	def rand_walkc(self):
 		return """
 /* 
 * File:   rand_walk.cpp
 * Author: Lucas Reynolds
 * Section 2 Project 6
 * March 10, 2014
 */

#include<random>
using std::default_random_engine; using std::uniform_int_distribution;
#include<map>
using std::map; using std::make_pair;
#include<vector>
using std::vector;
#include<string>
using std::string; using std::stol; using std::to_string;
#include<fstream>
using std::ifstream;
#include<iterator>
using std::iterator; using std::advance;

void read_index(map<long, string> &m, string &file_name) {
    /* reads the file_name in as an index file 
     * adds id (key) to website name (value) to the map
     * makes index_map
     */
    string site, id;
    ifstream infile;
    infile.open(file_name);
    if(infile.is_open()) {
        while (infile >> site >> id) {
            m.insert(make_pair(stol(id), site));
        }
    }
}

void read_arc(map<long, vector<long>> &m, string &file_name) {
    /* reads the file_name in as an arc_file
     * adds id (key) to vector of other sites that the id site maps to (value)
     * makes arc_map
     */
    string id, path;
    ifstream infile;
    infile.open(file_name);
    if(infile.is_open()) {
        vector <long> temp;
        while (infile >> id >> path) {
            if(m.find(stol(id)) != m.end()) { // in map then add to the vector
                m.at(stol(id)).push_back(stol(path));
            }
            else { // add the new key to the vector containing the first number.
                temp.push_back(stol(path)); 
                m.insert(make_pair(stol(id), temp));
                temp.clear();
            }
        }
    }
}

long select(default_random_engine &dre, vector<long> &container) {
    /* returns a random value from a vector of long. */
    uniform_int_distribution<> dist(0, container.size()-1);
    return container.at(dist(dre));
}

map<string, long> do_walk(map<long, vector<long>> &arc_map, map<long, string> &index_map,
                          long total_walks, long walk_length, default_random_engine &dre) {
    /* Does total_walks random walks of length walk_length.
     * Returns a visit_count map with key website_name and value visit_count.
     * calls select 
     */
    map <long, long> visit_count; // id/count
    map <string, long> out_visit_count; // website/count
    
    for(int j=0; j<total_walks; j++) {
        map<long, string>::iterator it=index_map.begin();
        uniform_int_distribution <> dist (0, index_map.size()-1); //finds a random node out of 105
        advance(it, dist(dre));
        long id = it->first;
        for(int i=0; i<walk_length-1; i++) { // -1 because the first value is a random node ^^
            if(visit_count.find(id) != visit_count.end()) { // if value is in the map
                visit_count[id] = visit_count.at(id) + 1;
            }
            else { // if value is not in the visit_count map
                visit_count[id] = 1;
            }
            if (arc_map.find(id) == arc_map.end()) { // if the next node does not have arcs
                visit_count[id] ++;
                break;
            }
            id = select(dre, arc_map[id]);
        }
    }
    for(auto itr=visit_count.begin(); itr!=visit_count.end(); itr++) {
        out_visit_count[index_map[itr->first]] = itr->second;
    }
    return out_visit_count;
}
"""
	def rand_walkh(self):
		return """
/* 
 * File:   rand_walk.h
 * Author: Lucas Reynolds
 * Section 2 Project 6
 * March 10, 2014
 */

#ifndef RAND_WALK_H
#define	RAND_WALK_H

#include<random>
using std::default_random_engine;
#include<map>
using std::map;
#include<vector>
using std::vector;
#include<string>
using std::string;

void read_index(map<long, string> &, string &);
void read_arc(map<long, vector<long>> &, string &);
long select(default_random_engine &, vector<long> &);
map<string, long> do_walk(map<long, vector<long>> &, map<long, string> &,
                          long total_walks, long walk_length, default_random_engine &);


#endif	/* RAND_WALK_H */
"""
	def schedulerc(self):
		return """
/* 
 * File:   scheduler.cpp
 * Author: Lucas Reynolds
 * Section 2 Project 9
 * April 7, 2014
 */

#include "scheduler.h"
#include "job.h"

#include <string>
using std::string;
#include <fstream>
using std::ifstream;
#include <vector>
using std::vector;
#include <algorithm>
using std::sort;
#include <iterator>
using std::iterator;
#include <iostream>
using std::cout; using std::endl;
#include <iomanip>
using std::setprecision; using std::setw; using std::fixed;

bool sort_arrival(Job one, Job two) {
    /* Sorts the vector jobs by arrival time if it can, otherwise by job id */
    if (one.get_arrival_time() == two.get_arrival_time())
        return one.get_job_id() < two.get_job_id();
    return one.get_arrival_time() < two.get_arrival_time();
}

void Scheduler::load_jobs(string file_name) {
    /* Constructs each job with the info from the file.
     * Sorts the vector even though they're already in order.*/
    int job_id, arrival_time, service_time;
    ifstream infile;
    infile.open(file_name);
    if (infile.is_open()) {
        while(infile >> job_id >> arrival_time >> service_time) {
            arrival_queue.push_back(Job(job_id, arrival_time, service_time));
        }
        sort(arrival_queue.begin(), arrival_queue.end(), sort_arrival);
    }
}

void Scheduler::round_robin() {
    /* Starts the clock and adds all of the jobs under the time.
     * Goes through each job if the service time equals zero, remove and set the finish time
     * otherwise the job gets added to the end of the processing_list.*/
    long time_clock = 0;
    while (!finished()) {
        bool checker = true;
        while (checker && !arrival_queue.empty()) {
            checker = false;
            if (arrival_queue.front().get_arrival_time() <= time_clock) {
                Job job = arrival_queue.front();
                arrival_queue.erase(arrival_queue.begin());
                processing_list.push_back(job);
                checker = true;
            }
        }
        int limit = processing_list.size();
        for(int i=0; i<limit; i++) {
            Job job = processing_list[0];
            processing_list.erase(processing_list.begin());
            if (job.get_time_left() == 0) {
                job.set_finish_time(time_clock);
                finished_jobs.push_back(job);
            }
            else {
                job.update_time_left(1);
                processing_list.push_back(job);
            }
        }
        time_clock += 1;
    }
}

bool Scheduler::finished() {
    /* Checks if both vectors are empty. */
    return arrival_queue.empty() && processing_list.empty();
}

void Scheduler::display() {
    /* Prints out the jobid, arrival_time, finish_time for each job.
     * Prints out the average finish_time-arrival_time and 65 char lines.*/
    cout << string(65, '-') << endl;
    cout << setw(15) << "JobID" << setw(15) <<"Arrival time" << setw(15) 
         << "Finish time" << endl;
    double total = 0;
    sort(finished_jobs.begin(), finished_jobs.end(), sort_arrival);
    for (auto job : finished_jobs) {
        cout << setw(12) << job.get_job_id() << setw(15) << job.get_arrival_time() 
             << setw(15) << job.get_finish_time() << endl;
        total += job.get_finish_time() - job.get_arrival_time();
    }
    cout << fixed << setprecision(2) << "The average amount of time to finish one job is " 
         << total/finished_jobs.size() << " time units." << endl;
    cout << string(65, '-') << endl;
}
"""
	def schedulerh(self):
		return """
 /* 
 * File:   scheduler.h
 * Author: Lucas Reynolds
 * Section 2 Project 9
 * April 7, 2014
 */

#ifndef SCHEDULER_H
#define	SCHEDULER_H

#include "job.h"
#include <string>
using std::string;
#include <vector>
using std::vector;
#include <map>
using std::map;

class Scheduler {
private:
    vector <Job> arrival_queue;
    vector <Job> processing_list;
    vector <Job> finished_jobs;
public:
    Scheduler() = default;
    
    void load_jobs(string file);
    void round_robin();
    bool finished();
    void display();
};


#endif	/* SCHEDULER_H */
"""