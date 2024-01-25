
@startuml
left to right direction
skinparam packageStyle rectangle
skinparam classAttributeIconSize 0

package "Model" {
 class MountModel {
  +List<MountData> mounts
  +MountData preferredMount
  +bool isAutoRideEnabled
 }
}

package "View" {
 class MountView {
  +ShowMountList()
  +ShowMountDetails(MountData mount)
  +ShowPreferredMounts()
  +ToggleAutoRide(bool enabled)
 }
 class MountRideWheelView {
  +DisplayRideWheel(List<MountData> preferredMounts)
 }
}

package "Controller" {
 class MountController {
  +RideMount(int mountId)
  +SetPreferredMount(int mountId)
  +GetMountData()
  +UpdateMountList()
  +UpdatePreferredMounts()
 }
}

package "NetSystem" {
 class NetSystem << (N,#87CEEB) >>
}

package "EventManager" {
 class EventManager << (E,#FFD700) >>
}

MountModel --> MountView : "Updates"
MountView --> MountController : "Events"
MountController --> MountModel : "Commands"
MountController --> EventManager : "Publish Events"
MountView --> EventManager : "AddListener"
NetSystem --> MountController : "Send Protocol"
MountController --> EventManager : "Listen for Events"
MountView --> EventManager : "Listen for Events"

class RideMountRequest {
 int32 mountId
}

class RideMountResponse {
 bool success
 string message
}

class SetPreferredMountRequest {
 int32 mountId
}

class SetPreferredMountResponse {
 bool success
 string message
}

class GetMountDataRequest {
}

class GetMountDataResponse {
 repeated MountData mounts
}

class MountData {
 int32 id
 string name
 bool isUnlocked
 bool isPreferred
 int32 runSpeed
 int32 flySpeed
 repeated string skillList
 string access
 string desc
}

NetSystem --> RideMountRequest : "Send/Receive"
NetSystem --> SetPreferredMountRequest : "Send/Receive"
NetSystem --> GetMountDataRequest : "Send/Receive"
NetSystem --> RideMountResponse : "Receive"
NetSystem --> SetPreferredMountResponse : "Receive"
NetSystem --> GetMountDataResponse : "Receive"

@enduml
