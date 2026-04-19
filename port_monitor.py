from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

mac_to_port = {}

# Switch connection
def _handle_ConnectionUp(event):
    log.info("Switch %s connected", event.dpid)
    mac_to_port[event.dpid] = {}


# PORT STATUS MONITORING
def _handle_PortStatus(event):
    port = event.ofp.desc.port_no
    state = event.ofp.desc.state

    if state & of.OFPPS_LINK_DOWN:
        log.info("⚠️ Port %s is DOWN", port)
    else:
        log.info("✅ Port %s is UP", port)


# LEARNING SWITCH LOGIC (FIXES YOUR ISSUE)
def _handle_PacketIn(event):
    packet = event.parsed
    dpid = event.dpid
    in_port = event.port

    if not packet.parsed:
        return

    src = packet.src
    dst = packet.dst

    # Learn source MAC
    mac_to_port[dpid][src] = in_port

    log.info("Packet: %s -> %s", src, dst)

    # If destination known → send directly
    if dst in mac_to_port[dpid]:
        out_port = mac_to_port[dpid][dst]
    else:
        out_port = of.OFPP_FLOOD

    # Send packet immediately
    msg = of.ofp_packet_out()
    msg.data = event.ofp
    msg.actions.append(of.ofp_action_output(port=out_port))
    event.connection.send(msg)

    # Install flow rule (only if known)
    if out_port != of.OFPP_FLOOD:
        flow_mod = of.ofp_flow_mod()
        flow_mod.match = of.ofp_match.from_packet(packet, in_port)
        flow_mod.actions.append(of.ofp_action_output(port=out_port))
        event.connection.send(flow_mod)


def launch():
    log.info("🚀 Port Monitoring + Learning Switch Controller Started")

    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    core.openflow.addListenerByName("PortStatus", _handle_PortStatus)
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)


