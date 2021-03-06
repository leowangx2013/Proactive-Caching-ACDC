//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
// 
// You should have received a copy of the GNU Lesser General Public License
// along with this program.  If not, see http://www.gnu.org/licenses/.
// 
/* @file MCD.cc
 * @author Johannes Pfannmüller, Christian Koch
 * @date
 * @version 1.0
 *
 * @brief Implements Move Copy Down Strategy
 *
 * @section DESCRIPTION
 *
 * This is a Class responsible for implementing the behaviour of the Move Copy Down Strategy.
 * Its main responsibility is to return a boolean value indicating if the video segment generated
 * a hit on the reverse proxy above in the topology and signaling the reverse proxy to store a copy
 * of this video segment. The reverseproxy above then deletes its copy of the video segment. It
 * basically "moves" the copy to another proxy.
 *
 */
#include "MCD.h"

MCD::MCD() {
    // TODO Auto-generated constructor stub

}

MCD::~MCD() {
    // TODO Auto-generated destructor stub
}

/**
 * @brief decides if the copy of a given video segment will be stored
 *
 * @param pkg is a pointer to an initialized VideoSegment
 * @return boolean signaling if a copy of the video segment should be stored
 */
bool MCD::toBeCached(VideoSegment* pkg) {
    if (pkg->getSeenAbove()) {
        pkg->setSeenAbove(false);
        return true;
    }
    return false;
}

/**
 * @brief periodic events
 *
 * @return void
 */
void MCD::periodicEvents() {

}
